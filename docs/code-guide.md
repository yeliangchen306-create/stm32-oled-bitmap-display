# 主要代码和函数说明

[返回 README](../README.md)

这部分只介绍程序中最常用的函数，不涉及太复杂的通信细节。

## 1. `main.c`

[`main.c`](../User/main.c) 是程序入口：

```c
OLED_Init();
OLED_ShowCartoon();
```

- `OLED_Init()`：初始化 OLED，让屏幕进入可以显示内容的状态；
- `OLED_ShowCartoon()`：把卡通点阵数组写入 OLED；
- `while (1)`：单片机程序不能直接结束，因此使用死循环让程序保持运行。

## 2. `OLED.c`

[`OLED.c`](../Hardware/OLED.c) 保存 OLED 的基础函数。这部分参考了 B 站江协科技的 STM32 OLED 教程。

### `OLED_I2C_Init()`

打开 GPIOB 时钟，并把 PB8、PB9 配置成开漏输出：

```c
PB8 → SCL
PB9 → SDA
```

后面的函数通过改变这两个引脚的高低电平，模拟 I²C 通信。

### `OLED_I2C_Start()` 和 `OLED_I2C_Stop()`

这两个函数产生 I²C 开始和停止信号。可以简单理解为：

```text
Start：告诉 OLED“接下来要发送内容了”
Stop：告诉 OLED“这次发送结束了”
```

### `OLED_I2C_SendByte()`

把一个 8 bit 数据从高位到低位发送给 OLED：

```c
OLED_W_SDA(!!(Byte & (0x80 >> i)));
```

这句代码每次取出 `Byte` 中的一位，再放到 SDA 数据线上。

### `OLED_WriteCommand()`

向 OLED 发送命令，例如设置显示方向、亮度和光标位置。

```c
OLED_I2C_SendByte(0x00);
```

其中 `0x00` 表示后面的内容是命令。

### `OLED_WriteData()`

向 OLED 发送真正要显示的点阵数据。

```c
OLED_I2C_SendByte(0x40);
```

其中 `0x40` 表示后面的内容是显示数据。

### `OLED_SetCursor(Y, X)`

设置接下来要从屏幕的哪个位置开始写数据：

- `Y` 的范围是 0～7，表示第几个 Page；
- `X` 的范围是 0～127，表示第几列。

这里的一个 Page 高 8 个像素，所以 64 像素高的屏幕共有 8 个 Page。

### `OLED_Clear()`

向整个屏幕写入 `0x00`，使所有像素熄灭。程序会遍历 8 个 Page，每页写 128 个字节。

### `OLED_ShowChar()`

显示一个 8×16 的字符。因为一个 Page 只有 8 像素高，所以一个字符要分成上、下两部分显示：

```text
前 8 字节  → 字符上半部分
后 8 字节  → 字符下半部分
```

### 其他显示函数

| 函数 | 用途 |
|---|---|
| `OLED_ShowString()` | 连续显示多个字符 |
| `OLED_ShowNum()` | 显示正整数 |
| `OLED_ShowSignedNum()` | 显示带正负号的整数 |
| `OLED_ShowHexNum()` | 显示十六进制数 |
| `OLED_ShowBinNum()` | 显示二进制数 |

这些函数最后都会调用 `OLED_ShowChar()`，把数字转换成对应字符后显示。

## 3. `OLED.h`

[`OLED.h`](../Hardware/OLED.h) 负责声明 OLED 函数。`main.c` 包含这个头文件后，就可以调用 `OLED_Init()` 等函数。

可以把它简单理解成一份“可使用功能清单”，真正的函数内容写在 `OLED.c` 中。

## 4. `OLED_Font.h`

[`OLED_Font.h`](../Hardware/OLED_Font.h) 保存 8×16 英文字符和数字的点阵数据。

例如显示字符 `A` 时，程序会通过：

```c
OLED_F8x16['A' - ' ']
```

找到 `A` 对应的 16 个字节，再把它们分成上下两页发送给 OLED。

## 5. `OLED_Cartoon.h`

[`OLED_Cartoon.h`](../Hardware/OLED_Cartoon.h) 是本项目新增的卡通图文件，里面主要有：

```c
static const uint8_t CartoonBitmap[1024];
```

这个数组保存整张 128×64 黑白图片。

`OLED_ShowCartoon()` 使用两层循环：

```c
for (page = 0; page < 8; page++)
{
    OLED_SetCursor(page, 0);

    for (x = 0; x < 128; x++)
    {
        OLED_WriteData(CartoonBitmap[page * 128 + x]);
    }
}
```

外层循环选择 8 个 Page，内层循环写入每页的 128 列，最终把 1024 字节全部显示出来。

