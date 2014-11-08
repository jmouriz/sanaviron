/*
 * interface.h -- GNU barcode/ECC200 ISO/IEC16022/POSTNET/QR interface for Python
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
#include "barcode.h"
#include "postnet.h"
#include "qrencode.h"
#include "iec16022ecc200.h"

#define DATAMATRIX 20
#define QR 21

char *barcode_get_code_data (int type, char *code, double width, double height);
char *barcode_get_text_data (int type, char *code);
char *qr_get_code_data (int type, char *code, double width, double height);
char *datamatrix_get_code_data (int type, char *code, double width, double height);
char *postnet_get_code_data (int type, char *code, double width, double height);
