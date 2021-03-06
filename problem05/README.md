<div dir="rtl">

# شهرک ترافیک

**مهارت‌های لازم:**

+ آشنایی با `JavaScript`

---

از آنجایی که تعداد خودروهای شهر بسیار زیاد شده، از شما می‌خواهیم تا برای مدیریت چراغ‌های راهنمایی به تیم ستاره کمک کنید. در ابتدا شما وظیفۀ مدیریت یک چهارراه را بر عهده دارید.

![خروجی نمونه](https://www.dropbox.com/s/v1ld5eqzb80vptc/problem05.jpg?dl=1)

# پروژه اولیه

پروژه اولیه را از [این لینک](https://quera.ir/contest/assignments/28171/download_problem_initial_project/94217) دانلود کنید.

<details class="blue">
<summary>ساختار فایل‌های این پروژه به این صورت است</summary>
```
initialProject05.zip
├── fonts
│   ├── samim-bold.ttf
│   ├── samim-medium.ttf
│   └── samim.ttf
├── data.json
├── index.html
├── main.js
├── main.css
└── traffic.js
```

</details>

<details class="pink">
<summary>راه اندازی پروژه</summary>

+ ابتدا پروژه‌ی اولیه را دانلود و از حالت فشرده خارج کنید.
+ سپس فایل `index.html` را در مرورگر خود باز کنید.

</details>

# جزئیات

چهارراه‌های شهرک ترافیک شامل چهار صفحه نمایش (_screen_) می‌باشند که هر کدام از سه چراغِ (_light_) قرمز، زرد و سبز تشکیل شده‌اند. شما باید با ایجاد تغییراتی در فایل `main.js`، بتنظیماتی که پلیس راهور به ما داده است را از فایل data.json بخوانید و با توجه به داده‌هایی که در پاسخ دریافت می‌کنید، زمانِ روشن‌بودنِ چراغ‌ها را تنظیم کنید. توجه داشته باشید، در زمان عملیاتی شدن فایل data.json تغییر می‌کند و شما نباید محتویات این فایل را به جای دیگری منتقل کنید.

می‌توانید نمونه‌ای از این فایل را در اینجا مشاهده کنید:

```json
{
    "timeline": {
        "top": [
            {
                "color": "red",
                "duration": 0
            },
            {
                "color": "green",
                "duration": 20
            },
            {
                "color": "yellow",
                "duration": 5
            },
            {
                "color": "red",
                "duration": 75
            }
        ],
        "right": [
            {
                "color": "red",
                "duration": 25
            },
            {
                "color": "green",
                "duration": 20
            },
            {
                "color": "yellow",
                "duration": 5
            },
            {
                "color": "red",
                "duration": 50
            }
        ],
        "bottom": [
            {
                "color": "red",
                "duration": 50
            },
            {
                "color": "green",
                "duration": 20
            },
            {
                "color": "yellow",
                "duration": 5
            },
            {
                "color": "red",
                "duration": 25
            }
        ],
        "left": [
            {
                "color": "red",
                "duration": 75
            },
            {
                "color": "green",
                "duration": 20
            },
            {
                "color": "yellow",
                "duration": 5
            },
            {
                "color": "red",
                "duration": 0
            }
        ]
    }
}
```

- در صورتی که پاسخ بالا به شما داده شود، خروجی مورد نظر [به این شکل](https://www.dropbox.com/s/frp0oviyl7ow3if/problem05%28timelapse%29.mp4?dl=0) خواهد بود.
(برای مشاهدۀ ویدئو کامل به [این لینک](https://www.dropbox.com/s/usduvc9692dh0k8/problem05.mp4?dl=0) مراجعه کنید.)
- داده‌ها به فرمت `JSON` به شما داده می‌شوند.
- زمانِ روشن‌بودن چراغ‌ها (_duration_) در واحد ثانیه است.

# راهنمایی

- برای رفع ابهامات احتمالی حتماً ویدئو بالا را مشاهده کنید. همچنین توصیه می‌کنیم قبل از شروع کار، فایل‌های `index.html` و `main.css` را بخوانید؛ هر چند که نباید تغییری در این فایل‌ها ایجاد کنید.
- با کلیکِ کاربر بر روی دکمۀ شروع، باید اطلاعات از سرور گرفته شود و وضعیت دکمه به `disabled` تغییر کند.
- صفحات نمایش به طور مستقل کار می‌کنند و شما فقط باید با توجه به زمان‌های در نظر گرفته شده، وضعیتِ هر یک را به طور جداگانه تغییر دهید.
- چراغ‌ها به طور پیشفرض روشن هستند و با اضافه‌کردنِ کلاسِ `off` به المانِ مربوطه، خاموش می‌شوند.
- زمانی که وضعیت یک صفحه نمایش تغییر می‌کند، باید متد `switchLight` را فراخوانی کنید. به عنوان مثال اگر وضعیت صفحه نمایش سمت راست به قرمز تغییر کند، باید از کد `switchLight('right', 'red')` استفاده کنید.
- در هر صفحه نمایش یک شمارشگر (_counter_) وجود دارد که باید در هر لحظه زمانِ باقی‌مانده تا تغییر وضعیتش را نشان دهد.
- شمارشگر هیچگاه نباید به عددِ صفر یا اعداد منفی برسد.
- به طور کلی می‌توان گفت با دریافت مدت زمان‌های روشن بودن هر چراغ هر سمت چهارراه، وظیفه دارید آن چراغ را به ترتیب و مدت زمان داده شده روشن نگه دارید. 

# توضیح مثال

برای مثال در داده‌ی داده شده در ابتدا برای چراغ سمت پایین 50 ثانیه به رنگ قرمز در می‌آید، بعد از آن 25 ثانیه به رنگ سبز و سپس 5 ثانیه به رنگ زرد و سپس 25 ثانیه به رنگ قرمز در می‌آید.

# نکات

+ تغییرات را تنها در فایل `main.js` اعمال کنید. تغییرات در باقی فایل‌ها نادیده گرفته می‌شود.
+ توجه کنید که داوری خودکار بر مبنای نام کلاس‌های فایل `index.html` انجام می‌شود.
+ پروژه را با ساختار زیر ارسال کنید.

```
[your-zip-file-name].zip
└── main.js
```

</div>
