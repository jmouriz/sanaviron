#define POSTNET_BAR_WIDTH      1.25
#define POSTNET_FULLBAR_HEIGHT 9.00
#define POSTNET_HALFBAR_HEIGHT 3.50
#define POSTNET_BAR_PITCH      3.25
#define POSTNET_HORIZ_MARGIN   9.00
#define POSTNET_VERT_MARGIN    3.00

enum
{
   POSTNET = 15,
   POSTNET_5,
   POSTNET_6,
   POSTNET_9,
   POSTNET_11,
   CEPNET
};

char *postnet_code (const char *code);

int check_valid_type (int type, const char *code);

void barcode_postnet (const char *type, double w, double h, const char *code);
