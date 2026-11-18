"""Build index.html for this article: one self-contained file with photos inlined.

Run from anywhere:  python3 web-summit-2026/build.py
Photos come from ./photos (already stripped of EXIF/GPS); the animated header
comes from ../shared/dancing-robots-header.html. Needs Pillow.
"""
import base64, io, re
from pathlib import Path
from PIL import Image

HERE = Path(__file__).parent
OUT_DIR = HERE
HEADER_FILE = HERE.parent / 'shared' / 'dancing-robots-header.html'

def img(n, long_edge=1000, q=70):
    im = Image.open(HERE / 'photos' / f'{n}.jpg').convert('RGB')
    im.thumbnail((long_edge, long_edge))
    buf = io.BytesIO(); im.save(buf, 'JPEG', quality=q, optimize=True)   # no EXIF/GPS kept
    return 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode()

def fig(n, cap, cls='half', pos='', extra=''):
    style = f' style="object-position:{pos}"' if pos else ''
    return (f'<figure class="{cls}">{extra}<img src="{img(n)}" alt="{cap}" loading="lazy"{style}>'
            f'<figcaption>{cap}</figcaption></figure>')

favicon = 'data:image/svg+xml;base64,' + base64.b64encode((HERE.parent / 'shared' / 'robot-favicon.svg').read_bytes()).decode()
header = re.search(r'<!-- HEADER:BEGIN.*?-->(.*?)<!-- HEADER:END -->',
                   HEADER_FILE.read_text(encoding='utf-8'), re.S).group(1)
header = (header.replace('Заголовок сторінки', 'Лісабон, роботи і шторм')
                .replace('Один рядок пояснення під заголовком.',
                         'Web Summit 2026 очима учасника: три дні з чотирьох, дев’ять танцюючих роботів і один шторм на ім’я «Шарль».'))

page = f'''<!DOCTYPE html>
<html lang="uk">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Лісабон, роботи і шторм — Web Summit 2026</title>
<meta name="description" content="Web Summit 2026 очима учасника: Лісабон до саміту, день роботів, скасована через шторм «Шарль» середа і фото з телефона.">
<meta property="og:type" content="article">
<meta property="og:url" content="https://peakodev.github.io/articles/web-summit-2026/">
<meta property="og:title" content="Лісабон, роботи і шторм">
<meta property="og:description" content="Web Summit 2026 очима учасника: Лісабон до саміту, день роботів, скасована через шторм «Шарль» середа і фото з телефона.">
<meta property="og:image" content="https://peakodev.github.io/articles/web-summit-2026/og.jpg?v=2">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="uk_UA">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Лісабон, роботи і шторм">
<meta name="twitter:description" content="Web Summit 2026 очима учасника: Лісабон до саміту, день роботів, скасована через шторм «Шарль» середа і фото з телефона.">
<meta name="twitter:image" content="https://peakodev.github.io/articles/web-summit-2026/og.jpg?v=2">
<link rel="icon" type="image/svg+xml" href="{favicon}">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Unbounded:wght@500;700&family=Golos+Text:wght@400;500;600;700&display=swap">
<style>
/* Layout: animated stage header, then a four-day diary; the cancelled day is the dark break in the middle. */
:root{{
  --bg:#f2f4fa; --surface:#ffffff; --ink:#0d1433; --muted:#5a6386; --line:#dde2ef;
  --blue:#1d4fd8; --coral:#d9432f; --storm-bg:#0b1130; --storm-ink:#e9edfb; --storm-muted:#a5aed0;
  --display:"Unbounded","Golos Text",system-ui,sans-serif;
  --body:"Golos Text",system-ui,-apple-system,"Segoe UI",sans-serif;
}}
@media (prefers-color-scheme: dark){{ :root{{
  --bg:#090e22; --surface:#121935; --ink:#eef1fb; --muted:#9aa3c6; --line:#262f57;
  --blue:#7d9bff; --coral:#ff806c; --storm-bg:#050818; color-scheme:dark }} }}
*{{box-sizing:border-box}}
body{{margin:0;overflow-x:clip;background:var(--bg);color:var(--ink);font-family:var(--body);font-size:17px;line-height:1.6}}
a{{color:var(--blue)}}
.wrap{{max-width:860px;margin:0 auto;padding-left:16px;padding-right:16px}}
main{{padding-block:28px 64px;display:flex;flex-direction:column;gap:44px}}
.lead{{font-size:1.18rem;max-width:62ch;margin:0}}
p{{max-width:65ch;margin:0}}
section{{display:flex;flex-direction:column;gap:16px}}
.day{{font-size:.78rem;letter-spacing:.12em;text-transform:uppercase;font-weight:600;color:var(--coral)}}
h2{{font-family:var(--display);font-weight:500;font-size:clamp(1.3rem,3.6vw,1.75rem);line-height:1.2;margin:0;text-wrap:balance}}
.facts{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:1px;background:var(--line);
  border:1px solid var(--line);border-radius:14px;overflow:hidden;font-variant-numeric:tabular-nums}}
.facts div{{background:var(--surface);padding:14px 16px}}
.facts b{{display:block;font-family:var(--display);font-weight:700;font-size:1.25rem}}
.facts span{{font-size:.84rem;color:var(--muted)}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:12px}}
figure{{margin:0;min-width:0;position:relative}}
.eggbox{{position:relative}}
.bye{{position:relative;display:flex;align-items:end;min-height:84px;padding:0 0 10px 100px;border-bottom:2px solid var(--line);color:var(--muted);font-size:.95rem}}
figure img{{display:block;width:100%;object-fit:cover;border-radius:12px;background:var(--line)}}
figure.wide{{grid-column:1/-1}}
figure.wide img{{aspect-ratio:16/9}}
figure.half img{{aspect-ratio:4/5}}
figcaption{{font-size:.84rem;color:var(--muted);margin-top:6px}}
.storm{{position:relative;background:var(--storm-bg);color:var(--storm-ink);border-radius:18px;padding:26px 22px}}
.storm .day{{color:#ff9a8a}}
.storm figcaption,.storm .src{{color:var(--storm-muted)}}
.storm ul{{margin:0;padding-left:1.1em;max-width:62ch}}
.storm li{{margin:6px 0}}
.take{{margin:0;padding-left:1.1em;max-width:65ch}}
.take li{{margin:8px 0}}
.sources{{font-size:.86rem;color:var(--muted)}}
.sources ul{{margin:8px 0 0;padding-left:1.1em}}
@media (max-width:520px){{ body{{font-size:16px}} .storm{{padding:22px 16px}} }}
</style>
</head>
<body>
{header}
<main class="wrap">
  <p class="lead">У програмі Web Summit 2026 було чотири дні: вечір відкриття та три дні павільйонів. На ділі вийшло три, бо середу в Лісабоні забрав шторм. Ми прилетіли на кілька днів раніше, тож нижче і місто, і саміт, і мої фото з телефона.</p>

  <div class="eggbox"><span class="dr-egg" data-pose="sit" data-acc="antenna" data-size="24" style="right:46px;top:0"></span>
  <div class="facts">
    <div><b>≈ 70 000</b><span>учасників</span></div>
    <div><b>164</b><span>країни</span></div>
    <div><b>900</b><span>спікерів</span></div>
    <div><b>2 000+</b><span>стартапів</span></div>
    <div><b>1 день</b><span>скасовано через шторм</span></div>
  </div></div>

  <section>
    <div class="day">5–8 листопада</div>
    <h2>Лісабон до саміту</h2>
    <p>Перші чотири дні були для міста. Почали з оглядових майданчиків Алфами: червоні дахи, Тежу і круїзний лайнер під самим пагорбом. Того ж дня переїхали на інший берег до статуї Христа, звідки найкраще видно міст 25 Квітня, а ввечері дійшли до Белена з підсвіченим пам’ятником Першовідкривачам.</p>
    <p>Далі був старий лісабонський трамвай, восьминіг на вечерю і день у Сінтрі. Палац Пена зустрів туманом і низькими хмарами. Тоді ми ще не знали, що це репетиція.</p>
    <div class="grid">
      {fig('c015','Алфама і Тежу з оглядового майданчика','wide','50% 40%')}
      {fig('c060','Під статуєю Христа на тому березі')}
      {fig('c084','Пам’ятник Першовідкривачам у Белені')}
      {fig('c063','Міст 25 Квітня з оглядового майданчика біля статуї','wide')}
      {fig('c111','У старому лісабонському трамваї')}
      {fig('c123','Восьминіг на вечерю')}
      {fig('c246','Палац Пена в Сінтрі','wide')}
    </div>
  </section>

  <section>
    <div class="day">Понеділок, 9 листопада</div>
    <h2>Відкриття в MEO Arena</h2>
    <p>Вечір відкриття: повна арена і знайома сцена з червоно-синіх світлових кубів. Преса назвала цей рік початком епохи «фізичного ШІ». Уперше людиноподібні роботи були зареєстровані як офіційні спікери саміту, а Китай привіз найбільшу делегацію за всі роки: понад 50 представників галузей ШІ та робототехніки.</p>
    <p>За даними Forbes, спікерами зареєстрували чотирьох роботів китайського виробництва: A3 і PrimeBOT Q1 від Agibot та G1 і ET1 від Galbot. Ще одна цифра з преси: за десять років саміт приніс економіці Португалії майже 2,5 млрд євро.</p>
    <p>Після офіційної частини всі перейшли на Night Summit: тунель із кубами під стелею, зала з парасольками і живий гурт на сцені.</p>
    <div class="grid">
      {fig('005','Центральна сцена, вечір відкриття','wide')}
      {fig('007','MEO Arena заповнена до верхніх рядів','half')}
      {fig('012','Дорога на Night Summit')}
      {fig('013','Стеля з парасольок на Night Summit')}
      {fig('017','Живий гурт на сцені Night Summit')}
    </div>
  </section>

  <section>
    <div class="day">Вівторок, 10 листопада</div>
    <h2 class="eggbox">День роботів<span class="dr-egg" data-pose="coffee" data-acc="phones" data-size="22" style="right:34px;bottom:0"></span></h2>
    <p>Павільйони FIL цього року більше скидалися на виставку робототехніки, ніж на конференцію про веб. Робопси ходили просто між людьми, гуманоїди танцювали в колі глядачів, а на Центральній сцені, за повідомленнями преси, дев’ять роботів AgiBot станцювали синхронно.</p>
    <p>Каву мені теж зварив робот: бариста Ella на стенді Intel Robotics, замовлення № 331, американо на ім’я Nazar.</p>
    <p>UBTECH привіз цілий стенд гуманоїдів під гаслом Dream with Robots, у зоні ALPHA стояв робот із двома маніпуляторами, а Atlassian поставив на стенді болід Формули-1. Навколо кожного робопса миттєво збиралося коло людей із телефонами.</p>
    <div class="grid">
      {fig('022','Робопес і гуманоїд на демо-майданчику','wide','50% 45%')}
      {fig('030','Гуманоїд танцює серед відвідувачів')}
      {fig('034','Фото з гуманоїдом UBTECH')}
      {fig('043','Робот-бариста на стенді Intel Robotics','wide')}
      {fig('045','Черга: «Nazar, Americano»')}
      {fig('048','Кава від робота і робопес у натовпі')}
      {fig('032','Стенд UBTECH: Dream with Robots')}
      {fig('049','Коло глядачів навколо робопса')}
      {fig('038','Гуманоїд на стенді в зоні ALPHA')}
      {fig('051','Болід на стенді Atlassian')}
    </div>
  </section>

  <section class="storm"><span class="dr-egg" data-pose="umbrella" data-size="24" style="right:60px;top:0"></span>
    <div class="day">Середа, 11 листопада</div>
    <h2>День, якого не було</h2>
    <p>Увечері 10 листопада організатори оголосили: програму середи скасовано. Причина — шторм «Шарль».</p>
    <ul>
      <li>Уряд Португалії порадив не проводити подію: ризик припливних підтоплень, збої громадського транспорту і сильний вітер, небезпечний для зовнішніх конструкцій.</li>
      <li>По всій материковій Португалії того дня закрили школи й неекстрені державні установи, країна була в стані підвищеної готовності на 24 години.</li>
      <li>За повідомленнями преси, в одному з павільйонів FIL протекла стеля.</li>
    </ul>
    <p>Ми встигли пройтися набережною Тежу вночі, поки вітер тільки здіймався, а сам шторм перечекали вдома з портвейном і виноградом.</p>
    <div class="grid">
      {fig('059','Набережна Тежу в ніч перед штормом','half','64% 50%')}
      {fig('057','План Б на штормовий день')}
    </div>
  </section>

  <section>
    <div class="day">Четвер, 12 листопада</div>
    <h2>Повернення і останній день</h2>
    <p>У четвер саміт відкрився знову. Galbot показував робота для автономного складу-магазину. На стендах ALPHA і BETA стояли стартапи із супутниковою аналітикою, морською робототехнікою та дронами.</p>
    <p>Поруч зі стартапами стояли великі гравці: Firefox зі скляним кубом Enterprise, європейська суперкомп’ютерна ініціатива EuroHPC, регіони й країни зі своїми павільйонами. Найпомітніший був у Азорських островів, із рибами під стелею.</p>
    <p>І фото на сцені з кубами, без нього поїздка не рахується.</p>
    <div class="grid">
      {fig('066','На сцені Web Summit')}
      {fig('064','Робот Galbot для автономного складу')}
      {fig('083','Стенд Invest Azores із рибами під стелею','wide','50% 40%','<span class="dr-egg" data-pose="peek" data-acc="shades" data-size="28" style="left:74%;top:0"></span>')}
      {fig('089','Стенд стартапу із супутниковою аналітикою, зона BETA')}
      {fig('085','Зона нетворкінгу між павільйонами')}
      {fig('088','Скляний куб Firefox Enterprise')}
      {fig('091','Стенд EuroHPC')}
    </div>
  </section>

  <section>
    <h2>Що варто запам’ятати</h2>
    <ul class="take">
      <li><strong>Тема року — фізичний ШІ.</strong> Роботи були не на слайдах, а на підлозі павільйонів і серед офіційних спікерів.</li>
      <li><strong>Дрони й робототехніка є серед стартапів ALPHA і BETA.</strong> Є з ким знайомитися і з ким себе порівнювати.</li>
      <li><strong>Погода забрала один із трьох днів павільйонів.</strong> Найважливіші зустрічі варто ставити на перший день.</li>
    </ul>
  </section>

  <div class="bye"><span class="dr-egg" data-pose="wave" data-acc="hat" data-size="26" style="left:44px;bottom:0"></span><p>Дякую, що дочитали. Роботів на цій сторінці можна хапати й тягати куди завгодно: клік — робот щось скаже, подвійний клік поверне його на місце.</p></div>

  <div class="sources">
    Фото автора, iPhone. Факти про саміт і шторм узято з публікацій:
    <ul>
      <li><a href="https://deadline.com/2026/11/web-summit-cancels-day-two-as-storm-charles-hits-lisbon-1237220064/">Deadline: Web Summit Cancels Day Two As Storm Charles Hits Portugal</a></li>
      <li><a href="https://www.portugal.fr/en/Storm-Charles-in-Portugal.html">Portugal closes schools and suspends Web Summit as Storm Charles brings severe weather</a></li>
      <li><a href="https://exhibitionnews.uk/rain-water-pours-down-from-ceiling-at-web-summit-organisers-cancel-day-two/">Exhibition News: Rain water pours down from ceiling at Web Summit</a></li>
      <li><a href="https://www.euronews.com/2026/11/09/web-summit-2026-in-lisbon-highlights-record-china-presence-and-robot-speakers-debut">Euronews: record China presence and robot speakers debut</a></li>
      <li><a href="https://www.africanews.com/2026/11/13/portugal-humanoid-robots-take-centre-stage-at-web-summit-2026/">Africanews: Humanoid robots take centre stage at Web Summit 2026</a></li>
      <li><a href="https://www.forbes.com/sites/johnkoetsier/2026/11/10/robot-trash-talk-at-web-summit-as-agibot-disses-tesla-figure-unitree/">Forbes: Robot Trash Talk At Web Summit</a></li>
    </ul>
  </div>
</main>
</body>
</html>
'''
out = OUT_DIR / 'index.html'
out.write_text(page, encoding='utf-8')
print(out, round(out.stat().st_size / 1e6, 2), 'MB')
