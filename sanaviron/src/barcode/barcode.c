/*
 * barcode.c -- GNU barcode/ECC200 ISO/IEC16022/POSTNET interface for Python
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
#include "interface.h"

char *
get_code_data (int type, char *code, double width, double height)
{
   if (type < POSTNET)
   {
      return barcode_get_code_data (type, code, width, height);
   }
   else if (type < DATAMATRIX)
   {
      return postnet_get_code_data (type, code, width, height);
   }
   else if (type == DATAMATRIX)
   {
      return datamatrix_get_code_data (type, code, width, height);
   }
   else if (type == QR)
   {
      return qr_get_code_data (type, code, width, height);
   }

   return NULL;
}

char *
get_text_data (int type, char *code)
{
   if (type > BARCODE_93)
   {
      return NULL;
   }

   return barcode_get_text_data (type, code);
}
