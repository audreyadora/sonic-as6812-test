
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/init.h>
#include <linux/platform_device.h>
#include <linux/err.h>
#include <linux/leds.h>
#include <linux/slab.h>
#include <linux/dmi.h>

/* led_type: 0=loc, 1=diag, 2=fan, 3=psu1, 4=psu2
 * light_mode: 0=off, 1=green, 2=amber, 3=blinking green
 */
extern int dbmvtx9180_fpga_sysled_get(int led_type);
extern int dbmvtx9180_fpga_sysled_set(int led_type, int light_mode);

#define DRVNAME "marvell_dbmvtx9180_led"

struct marvell_dbmvtx9180_led_data {
    struct platform_device *pdev;
    struct mutex           lock;
    int                    sysled_status[5];
};

static struct marvell_dbmvtx9180_led_data  *ledctl = NULL;

/* LED related data */
#define LED_MODE_OFF_VALUE              0
#define LED_MODE_GREEN_VALUE            1
#define LED_MODE_AMBER_VALUE            2
#define LED_MODE_BLK_GREEN_VALUE        3

enum led_type {
    LED_TYPE_LOC,
    LED_TYPE_DIAG,
    LED_TYPE_FAN,
    LED_TYPE_PSU1,
    LED_TYPE_PSU2,
    LED_TYPE_END
};

enum led_light_mode {
    LED_MODE_OFF = 0,
    LED_MODE_GREEN,
    LED_MODE_AMBER,
    LED_MODE_BLK_GREEN,
    LED_MODE_UNKNOWN
};

static void marvell_dbmvtx9180_led_update(void)
{
    int i;
    mutex_lock(&ledctl->lock);
    for (i = 0; i < LED_TYPE_END; i++)
    {
        ledctl->sysled_status[i] = dbmvtx9180_fpga_sysled_get(i);
    }
    mutex_unlock(&ledctl->lock);
}

static void marvell_dbmvtx9180_led_set(struct led_classdev *led_cdev,
                                       enum led_brightness led_light_mode,
                                       enum led_type type)
{
    mutex_lock(&ledctl->lock);
    dbmvtx9180_fpga_sysled_set(type, led_light_mode);
    mutex_unlock(&ledctl->lock);
}

static void marvell_dbmvtx9180_led_diag_set(struct led_classdev *led_cdev,
                                            enum led_brightness led_light_mode)
{
    marvell_dbmvtx9180_led_set(led_cdev, led_light_mode, LED_TYPE_DIAG);
}

static enum led_brightness marvell_dbmvtx9180_led_diag_get(struct led_classdev *cdev)
{
    marvell_dbmvtx9180_led_update();
    return ledctl->sysled_status[LED_TYPE_DIAG];
}

static void marvell_dbmvtx9180_led_loc_set(struct led_classdev *led_cdev,
                                           enum led_brightness led_light_mode)
{
    marvell_dbmvtx9180_led_set(led_cdev, led_light_mode, LED_TYPE_LOC);
}

static enum led_brightness marvell_dbmvtx9180_led_loc_get(struct led_classdev *cdev)
{
    marvell_dbmvtx9180_led_update();
    return ledctl->sysled_status[LED_TYPE_LOC];
}

static void marvell_dbmvtx9180_led_fan_set(struct led_classdev *led_cdev,
                                           enum led_brightness led_light_mode)
{
    marvell_dbmvtx9180_led_set(led_cdev, led_light_mode, LED_TYPE_FAN);
}

static enum led_brightness marvell_dbmvtx9180_led_fan_get(struct led_classdev *cdev)
{
    marvell_dbmvtx9180_led_update();
    return ledctl->sysled_status[LED_TYPE_FAN];
}

static void marvell_dbmvtx9180_led_psu1_set(struct led_classdev *led_cdev,
                                            enum led_brightness led_light_mode)
{
    marvell_dbmvtx9180_led_set(led_cdev, led_light_mode, LED_TYPE_PSU1);
}

static enum led_brightness marvell_dbmvtx9180_led_psu1_get(struct led_classdev *cdev)
{
    marvell_dbmvtx9180_led_update();
    return ledctl->sysled_status[LED_TYPE_PSU1];
}

static void marvell_dbmvtx9180_led_psu2_set(struct led_classdev *led_cdev,
                                            enum led_brightness led_light_mode)
{
    marvell_dbmvtx9180_led_set(led_cdev, led_light_mode, LED_TYPE_PSU2);
}

static enum led_brightness marvell_dbmvtx9180_led_psu2_get(struct led_classdev *cdev)
{
    marvell_dbmvtx9180_led_update();
    return ledctl->sysled_status[LED_TYPE_PSU2];
}

static struct led_classdev marvell_dbmvtx9180_leds[] = {
    [LED_TYPE_DIAG] = {
        .name            = "marvell_dbmvtx9180_led::diag",
        .default_trigger = "unused",
        .brightness_set  = marvell_dbmvtx9180_led_diag_set,
        .brightness_get  = marvell_dbmvtx9180_led_diag_get,
        .flags           = LED_CORE_SUSPENDRESUME,
        .max_brightness  = LED_MODE_BLK_GREEN,
    },
    [LED_TYPE_LOC] = {
        .name            = "marvell_dbmvtx9180_led::loc",
        .default_trigger = "unused",
        .brightness_set  = marvell_dbmvtx9180_led_loc_set,
        .brightness_get  = marvell_dbmvtx9180_led_loc_get,
        .flags           = LED_CORE_SUSPENDRESUME,
        .max_brightness  = LED_MODE_BLK_GREEN,
    },
    [LED_TYPE_FAN] = {
        .name            = "marvell_dbmvtx9180_led::fan",
        .default_trigger = "unused",
        .brightness_set  = marvell_dbmvtx9180_led_fan_set,
        .brightness_get  = marvell_dbmvtx9180_led_fan_get,
        .flags           = LED_CORE_SUSPENDRESUME,
        .max_brightness  = LED_MODE_AMBER,
    },
    [LED_TYPE_PSU1] = {
        .name            = "marvell_dbmvtx9180_led::psu1",
        .default_trigger = "unused",
        .brightness_set  = marvell_dbmvtx9180_led_psu1_set,
        .brightness_get  = marvell_dbmvtx9180_led_psu1_get,
        .flags           = LED_CORE_SUSPENDRESUME,
        .max_brightness  = LED_MODE_AMBER,
    },
    [LED_TYPE_PSU2] = {
        .name            = "marvell_dbmvtx9180_led::psu2",
        .default_trigger = "unused",
        .brightness_set  = marvell_dbmvtx9180_led_psu2_set,
        .brightness_get  = marvell_dbmvtx9180_led_psu2_get,
        .flags           = LED_CORE_SUSPENDRESUME,
        .max_brightness  = LED_MODE_AMBER,
    },
};

static int marvell_dbmvtx9180_led_suspend(struct platform_device *dev,
                                          pm_message_t state)
{
    int i = 0;

    for (i = 0; i < ARRAY_SIZE(marvell_dbmvtx9180_leds); i++)
    {
        led_classdev_suspend(&marvell_dbmvtx9180_leds[i]);
    }

    return 0;
}

static int marvell_dbmvtx9180_led_resume(struct platform_device *dev)
{
    int i = 0;

    for (i = 0; i < ARRAY_SIZE(marvell_dbmvtx9180_leds); i++)
    {
        led_classdev_resume(&marvell_dbmvtx9180_leds[i]);
    }

    return 0;
}

static int marvell_dbmvtx9180_led_probe(struct platform_device *pdev)
{
    int ret, i;

    for (i = 0; i < ARRAY_SIZE(marvell_dbmvtx9180_leds); i++)
    {
        ret = led_classdev_register(&pdev->dev, &marvell_dbmvtx9180_leds[i]);

        if (ret < 0)
            break;
    }

    /* Check if all LEDs were successfully registered */
    if (i != ARRAY_SIZE(marvell_dbmvtx9180_leds))
    {
        int j;

        /* only unregister the LEDs that were successfully registered */
        for (j = 0; j < i; j++)
        {
            led_classdev_unregister(&marvell_dbmvtx9180_leds[i]);
        }
    }

    return ret;
}

static int marvell_dbmvtx9180_led_remove(struct platform_device *pdev)
{
    int i;

    for (i = 0; i < ARRAY_SIZE(marvell_dbmvtx9180_leds); i++)
    {
        led_classdev_unregister(&marvell_dbmvtx9180_leds[i]);
    }

    return 0;
}

static struct platform_driver marvell_dbmvtx9180_led_driver = {
    .probe    = marvell_dbmvtx9180_led_probe,
    .remove   = marvell_dbmvtx9180_led_remove,
    .suspend  = marvell_dbmvtx9180_led_suspend,
    .resume   = marvell_dbmvtx9180_led_resume,
    .driver   = {
        .name   = DRVNAME,
        .owner  = THIS_MODULE,
    },
};

static int __init marvell_dbmvtx9180_led_init(void)
{
    int ret;

    ret = platform_driver_register(&marvell_dbmvtx9180_led_driver);
    if (ret < 0)
    {
        goto exit;
    }

    ledctl = kzalloc(sizeof(struct marvell_dbmvtx9180_led_data), GFP_KERNEL);
    if (!ledctl)
    {
        ret = -ENOMEM;
        platform_driver_unregister(&marvell_dbmvtx9180_led_driver);
        goto exit;
    }

    mutex_init(&ledctl->lock);

    ledctl->pdev = platform_device_register_simple(DRVNAME, -1, NULL, 0);
    if (IS_ERR(ledctl->pdev))
    {
        ret = PTR_ERR(ledctl->pdev);
        platform_driver_unregister(&marvell_dbmvtx9180_led_driver);
        kfree(ledctl);
        goto exit;
    }

exit:
    return ret;
}

static void __exit marvell_dbmvtx9180_led_exit(void)
{
    platform_device_unregister(ledctl->pdev);
    platform_driver_unregister(&marvell_dbmvtx9180_led_driver);
    kfree(ledctl);
}

module_init(marvell_dbmvtx9180_led_init);
module_exit(marvell_dbmvtx9180_led_exit);

MODULE_AUTHOR("Krishnan Sridharan <ksridharan@marvell.com>");
MODULE_DESCRIPTION("marvell_dbmvtx9180_led driver");
MODULE_LICENSE("GPL");
