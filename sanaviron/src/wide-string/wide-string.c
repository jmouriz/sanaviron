/*
 * wide-string.c - Very simple multi-byte sequences manipulation interface
 *                 for Python.
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

/* http://tools.ietf.org/html/rfc3629 */

/* count_bytes determine the lenght of byte in a multi-byte sequence. This
 * lenght can be from 1 to 6 in UTF-8.
 *
 * An important property of the coding is that the more significative bits of
 * first byte of a multi-byte sequence determine the lenght of symbol. So
 * this function count the first four bits of a given byte until these are
 * one's.
 *
 * Explain can be found at http://es.wikipedia.org/wiki/UTF-8 (in spanish).
 */
int
count_bytes (char byte)
{
   int count;
   int bit;

   count = 0;
   bit = 0;

   while (bit <= 4)
   {
      if (((byte << bit++) & 0x80) == 0x80) /* if the bit is in one */
      {
         count++;
      }
      else
      {
         break;
      }
   }

   return count;
}

/* get_cursor_position get the real cursor position in an UTF-8 string.
 *
 * Because UTF-8 strings are multi-byte sequences, the cursor position not
 * always is the real digit position. So this function get the real position
 * given an "index" on the string.
 */
int
get_cursor_position (char *string, int position)
{
   int wides;
   int count;
   int bytes;

   count = -1;
   wides = 0;

   while (string[++count] && count < (position + wides))
   {
      if (string[count] < 0) /* if byte is multi-byte */
      {
         bytes = count_bytes (string[count]) - 1; /* get multi-byte size in bytes. */
                                                  /* -1 is because one byte is already */
                                                  /* counted in condition for ASCII bytes */

         wides += bytes;
         count += bytes;
      }
   }

   return count;
}
