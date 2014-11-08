#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <ctype.h>
#include "postnet.h"

static char *symbols[] =
{
	/* 0 */ "11000",
	/* 1 */ "00011",
	/* 2 */ "00101",
	/* 3 */ "00110",
	/* 4 */ "01001",
	/* 5 */ "01010",
	/* 6 */ "01100",
	/* 7 */ "10001",
	/* 8 */ "10010",
	/* 9 */ "10100"
};

static char *frame = "1";

static int is_length_valid (const char *code, int length);

static int check_valid (const char *type, const char *code);

char *
postnet_code (const char *code)
{
   int lenght;
   int offset;
   int sum;
   char *digit;
   char *buffer;

   buffer = (char *) malloc (8 + 5 * 11);
   *buffer = 0;
   sum = 0;

   /* Left frame bar */
   strcat (buffer, frame);

   for (digit = (char *) code, lenght = 0; (*digit != 0) && (lenght < 11); digit++)
   {
      if (isdigit (*digit))
      {
         /* Only translate valid characters (0-9) */
         offset = (*digit) - '0';
         sum += offset;
         strcat (buffer, symbols[offset]);
         lenght++;
      }
   }

   /* Create correction character */
   offset = (10 - (sum % 10)) % 10;
   strcat (buffer, symbols[offset]);

   /* Right frame bar */
   strcat (buffer, frame);

   return buffer;
}

int
check_valid_type (int type, const char *code)
{
   switch (type)
   {
      case POSTNET:    return check_valid ("POSTNET",    code);
      case POSTNET_5:  return check_valid ("POSTNET-5",  code);
      case POSTNET_6:  return check_valid ("POSTNET-6",  code);
      case POSTNET_9:  return check_valid ("POSTNET-9",  code);
      case POSTNET_11: return check_valid ("POSTNET-11", code);
      case CEPNET:     return check_valid ("CEPNET",     code);
      default:         return 0;
   };
}

static int
check_valid (const char *type, const char *code)
{
	/* Validate code length for all subtypes. */
	if ((strcasecmp (type, "POSTNET") == 0))
		if (!is_length_valid (code, 5) &&
		    !is_length_valid (code, 6) &&
		    !is_length_valid (code, 9) &&
		    !is_length_valid (code, 11))
			return 0;
	if ((strcasecmp (type, "POSTNET-5") == 0))
		if (!is_length_valid (code, 5))
			return 0;
	if ((strcasecmp (type, "POSTNET-6") == 0))
		if (!is_length_valid (code, 6))
			return 0;
	if ((strcasecmp (type, "POSTNET-9") == 0))
		if (!is_length_valid (code, 9))
			return 0;
	if ((strcasecmp (type, "POSTNET-11") == 0))
		if (!is_length_valid (code, 11))
			return 0;
	if ((strcasecmp (type, "CEPNET") == 0))
		if (!is_length_valid (code, 8))
			return 0;

	return 1;
}


static int
get_code_lenght (const char *code)
{
	char *digit;
	int count;

	if (!code)
	{
		return 0;
	}

	for (digit = (char *) code, count = 0; *digit != 0; digit++)
	{
		/* Only count valid characters (0-9) */
		if (isdigit (*digit))
		{
			count++;
		}
	}

	return count;
}

static int
is_length_valid (const char *code, int length)
{
	return (get_code_lenght (code) == length);
}
