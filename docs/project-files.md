# 工程文件说明

[返回 README](../README.md)

## `Start` 文件夹

保存 STM32 启动文件、Cortex-M3 内核文件和系统初始化代码。单片机复位后，会先执行启动文件，再进入 `main()`。

这部分来自 STM32 工程模板，初学阶段一般不需要修改。

## `Library` 文件夹

保存 STM32F10x 标准外设库，例如 GPIO、RCC、定时器和串口等驱动。

本项目直接使用了：

- RCC：打开 GPIOB 外设时钟；
- GPIO：控制 PB8 和 PB9 的高低电平。

标准外设库和工程模板参考了 B 站江协科技的 STM32 入门教程。库文件自身保留了 STMicroelectronics 的原始文件声明。

## `User` 文件夹

- `main.c`：程序入口；
- `stm32f10x_conf.h`：选择需要包含的标准外设库头文件；
- `stm32f10x_it.c/.h`：中断函数模板。

## `Hardware` 文件夹

- `OLED.c`：OLED 基础驱动和显示函数；
- `OLED.h`：OLED 函数声明；
- `OLED_Font.h`：8×16 字符点阵；
- `OLED_Cartoon.h`：自定义卡通图片点阵。

OLED 基础驱动、字模和显示函数参考了 B 站江协科技教程；卡通点阵数组和 `OLED_ShowCartoon()` 是本项目在学习基础代码后增加的内容。

## `Project.uvprojx`

Keil 工程文件。双击它可以直接打开项目。

GitHub 版本已经移除了原工程中没有使用的 LED、Key 和 Delay 模块引用。

## 没有上传的文件

以下内容属于编译产物或个人开发环境文件，没有必要放到 GitHub：

```text
Objects/
Listings/
DebugConfig/
*.axf
*.hex
*.bin
*.uvguix.*
```

这些文件可以由 Keil 重新生成，上传后反而会让仓库显得杂乱。

