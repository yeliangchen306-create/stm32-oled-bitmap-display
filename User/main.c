#include "stm32f10x.h"                  // Device header
#include "OLED.h"
#include "OLED_Cartoon.h"

int main(void)
{
	OLED_Init();
	OLED_ShowCartoon();

	while (1)
	{
	}
}
