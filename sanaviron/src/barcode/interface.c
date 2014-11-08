/*
 * interface.c -- GNU barcode/ECC200 ISO/IEC16022/POSTNET/QR interface for Python
 *
 * Copyright (c) 2012 Juan Manuel Mouriz (jmouriz@sanaviron.org)
 *
 *  This program is free software; you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation; either version 2 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program; if not, write to the Free Software
 *  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 */
#include <stdlib.h>
#include <string.h>

#include "interface.h"

#define MIN_PIXEL_SIZE  1.0
#define POSTNET_MARGINS 0

char *
barcode_get_code_data (int type, char *code, double width, double height)
{
   struct Barcode_Item *barcode;
   char *output;
   double ratio;
   double lenght;
   double x;
   double y;
   int flags;
   int count;
   int size;
   int bar;
   int i;

   if (strlen (code) == 0)
   {
      return NULL;
   }

   flags = type | BARCODE_OUT_PS | BARCODE_OUT_NOHEADERS;
   barcode = Barcode_Create (code);

   Barcode_Encode (barcode, flags);

   if (barcode->error)
   {
      return NULL;
   }

   /* from:int svg_bars(struct Barcode_Item *bc, FILE *f) */
   count = strlen (barcode->partial);
   x = 0;    /* Where the current box is drawn on x */
   y = 0;    /* Where the current box is drawn on y */
   i = 0;    /* Loop counter */
   bar = 0;
   size = 0;

   output = (char *) malloc (8 + 36 * count);

   while (i < count)
   {
      char current = *(barcode->partial + i) - 48;

      if (current > 9)
      {
         if (i + 1 >= count)
         {
            break;
         }

         current = *(barcode->partial + i + 1) - 48;
         i += 2;
      }

      x += current;
      i++;
   }

   ratio = width / x;
   i = 0;
   x = 0;

   while (i < count)
   {
      char current = *(barcode->partial + i) - 48;

      lenght = height; /* Guide bar */

      if (current > 9)
      {
         if (i + 1 >= count)
         {
            break;
         }

         current = *(barcode->partial + i + 1) - 48;
         i += 2;
      }
      else
      {
         lenght -= 20;
      }

      if (bar)
      {
         sprintf (output + size, "%.02f:%.02f:%.02f:%.02f ", x, y, current * ratio, lenght);
         size = strlen (output);
         bar = 0;
      }
      else
      {
         bar = 1;
      }

      x += current * ratio;
      i++;
   }
   /* from:int svg_bars(struct Barcode_Item *bc, FILE *f) */

   sprintf (output + size, "%.02f", ratio);

   return output;
}

char *
barcode_get_text_data (int type, char *code)
{
   struct Barcode_Item *barcode;
   int flags;

   if (strlen (code) == 0)
   {
      return NULL;
   }

   flags = type | BARCODE_OUT_PS | BARCODE_OUT_NOHEADERS;

   barcode = Barcode_Create (code);

   Barcode_Encode (barcode, flags);

   if (barcode->error)
   {
      return NULL;
   }

   *(barcode->textinfo + strlen (barcode->textinfo) - 1) = '\0';

   return barcode->textinfo;
}

char *
datamatrix_get_code_data (int type, char *code, double width, double height)
{
   char *grid;
   char *output;
   double ratio;
   double pixel;
   int size;
   int w;
   int h;
   int i;
   int j;

   if (strlen (code) == 0)
   {
      return NULL;
   }

   w = 0;
   h = 0;

   grid = (char *) iec16022ecc200 (&w, &h, NULL, strlen (code), (unsigned char *) code, NULL, NULL, NULL);

   output = (char *) malloc (8 + 36 * w * h);
   size = 0;

   /* Treat requested size as a bounding box, scale to maintain aspect ratio while fitting it in this box
    * and determine the pixel size
    */
   ratio = (double) h / (double) w;

   pixel = ((height < width * ratio) ? height / ratio : width) / w;

   if (pixel < MIN_PIXEL_SIZE)
   {
      pixel = MIN_PIXEL_SIZE;
   }

   /* Now traverse the code string and create a list of boxes */
   for (i = h - 1; i >= 0; i--)
   {
      for (j = 0; j < w; j++)
      {
         if (*grid++)
         {
            double x = j * pixel + pixel / 2.0;
            double y = i * pixel;
            double length = pixel;
            double thickness = pixel;

            sprintf (output + size, "%.02f:%.02f:%.02f:%.02f ", x, y, thickness, length);
            size = strlen (output);
         }
      }
   }

   sprintf (output + size, "%.02f", 0.0);

   return output;
}

char *
postnet_get_code_data (int type, char *code, double width, double height)
{
   char *buffer;
   char *digit;
   char *output;
   double horiz_margin;
   double vert_margin;
   double bar_width;
   double full_height;
   double half_height;
   double bar_pitch;
   double a;
   double w;
   double h;
   int size;

   if (strlen (code) == 0)
   {
      return NULL;
   }

   /* Validate code length for all subtypes */
   if (!check_valid_type (type, (const char *)  code))
   {
      return NULL;
   }

   /* First get code string */
   buffer = postnet_code (code);

   if (buffer == NULL)
   {
      return NULL;
   }

   w = 2 * POSTNET_HORIZ_MARGIN * POSTNET_MARGINS + strlen (buffer) * POSTNET_BAR_PITCH;
   h = 2 * POSTNET_VERT_MARGIN * POSTNET_MARGINS + POSTNET_FULLBAR_HEIGHT;

   horiz_margin = POSTNET_HORIZ_MARGIN * width / w;
   vert_margin = POSTNET_VERT_MARGIN * height / h;
   bar_width = POSTNET_BAR_WIDTH * width / w;
   full_height = POSTNET_FULLBAR_HEIGHT * height / h;
   half_height = POSTNET_HALFBAR_HEIGHT * height / h;
   bar_pitch = POSTNET_BAR_PITCH * width / w;

   horiz_margin *= POSTNET_MARGINS;
   vert_margin *= POSTNET_MARGINS;

   output = (char *) malloc (8 + 36 * strlen (buffer));
   size = 0;

   /* Now traverse the code string and create a list of lines */
   a = horiz_margin;

   for (digit = buffer; *digit != 0; digit++)
   {
      double x = a;
      double y = vert_margin;
      double thickness = bar_width;
      double length;

      if (*digit == '0')
      {
         y += full_height - half_height;
         length = half_height;
      }
      else
      {
         length = full_height;
      }

      sprintf (output + size, "%.02f:%.02f:%.02f:%.02f ", x, y, thickness, length);
      size = strlen (output);
      a += bar_pitch;
   }

   sprintf (output + size, "%.02f", 0.0);

   return output;
}

char *
qr_get_code_data (int type, char *code, double width, double height)
{
	QRecLevel level;
	QRencodeMode hint;
	QRcode *encoded;
	unsigned char *row;
	char *output;
	double pixel;
	int sensitive;
	int eightbit;
	int version;
	int structured;
	int micro;
	int size;
	int i;
	int j;

	if (strlen (code) == 0)
	{
		return NULL;
	}

   /* Hardcoded parameters */
	sensitive = 1;			/* Encode lower-case alphabet characters in 8-bit mode. 		*/
	eightbit = 0;			/* Encode entire data in 8-bit mode. 							*/
	version = 0;			/* Specify the version of the symbol. => 0: AUTOMATIC  			*/
							/* 			QRSPEC_VERSION_MIN, QRSPEC_VERSION_MAX,   			*/
							/*			MQRSPEC_VERSION_MIN, MQRSPEC_VERSION_MAX  			*/
	structured = 0;			/* Make structured symbols. Version must be specified. 			*/
	micro = 0;				/* Encode in a Micro QR Code. (experimental). 					*/
	level = QR_ECLEVEL_L; 	/* Error correction level from L (lowest) to H (highest). =>	*/
							/*			QR_ECLEVEL_L, QR_ECLEVEL_M, QR_ECLEVEL_Q,			*/
							/*			QR_ECLEVEL_H 										*/
	hint = QR_MODE_8; 		/* Encoder hints. => QR_MODE_8, QR_MODE_KANJI 					*/
	size = strlen (code);

	if (micro)
	{
		if (eightbit)
		{
			encoded = QRcode_encodeDataMQR (size, (unsigned char *) code, version, level);
		}
		else
		{
			encoded = QRcode_encodeStringMQR ((char *) code, version, level, hint, sensitive);
		}
	}
	else
	{
		if (eightbit)
		{
			encoded = QRcode_encodeData (size, (unsigned char *)code, version, level);
		}
		else
		{
			encoded = QRcode_encodeString ((char *) code, version, level, hint, sensitive);
		}
	}

	if (!encoded)
	{
		return NULL;
	}

	output = (char *) malloc (8 + 36 * encoded->width * encoded->width);
	size = 0;

	if (output == NULL)
	{
		fprintf (stderr, "Failed to allocate memory.\n");
		return NULL;
	}

	pixel = width / encoded->width;

	for (i = 0; i < encoded->width; i++)
	{
		row = encoded->data + i * encoded->width;

		for (j = 0; j < encoded->width; j++)
		{
			if (row[j] & 0x1)
			{
				double x = j * pixel + pixel / 2.0;
				double y = i * pixel;
				double thickness = pixel;
				double length = pixel;

				sprintf (output + size, "%.02f:%.02f:%.02f:%.02f ", x, y, thickness, length);
				size = strlen (output);
			}
		}
	}

	sprintf (output + size, "%.02f", 0.0);

	QRcode_free (encoded);

	return output;
}
