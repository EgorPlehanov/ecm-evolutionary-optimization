### Elliptic Curve Method (Lenstra, 1987)
- Файл: [1__factoring-integers-with-elliptic-curves-lenstra-1987.md](./markdown/0__main/1__factoring-integers-with-elliptic-curves-lenstra-1987.md)
- Тема: Оригинальное описание метода факторизации на эллиптических кривых (ECM), обобщающего метод Полларда p−1, и анализ его сложности.
- Summary (EN): Original ECM paper. Replaces (Z/pZ)* with group of random elliptic curve E(F_p) of order p+1−t. Success when order is B‑smooth. Uses Deuring's formula to count curves with given order. Conjectured complexity L(p)^{√2+o(1)} M(n) where L(x)=exp(√(log x log log x)). Storage O(log n). Faster than QS when n has small factor. Heuristic relies on smooth number distribution in short intervals.
- Сводка (RU): Оригинальная работа по ECM. Замена (Z/pZ)* на группу случайной эллиптической кривой порядка p+1−t. Успех при B‑гладком порядке. Использование формулы Дойринга для подсчёта кривых с заданным порядком. Предполагаемая сложность L(p)^{√2+o(1)} M(n). Память O(log n). Быстрее QS при наличии малого делителя. Эвристика опирается на распределение гладких чисел в коротких интервалах.
- Ключевые слова: ECM, elliptic curve method, integer factorization, Lenstra, Pollard p−1, smooth numbers, Deuring formula, Hasse theorem
- ГОСТ: Lenstra Jr. H. W. Factoring integers with elliptic curves // Annals of Mathematics. – 1987. – Vol. 126, No. 3. – P. 649–673. – DOI: 10.2307/1971363.

---

### Pollard p−1 method and theoretical factoring (Pollard, 1974)
- Файл: [2__pollard-p-minus-1-and-rho-1974.md](./markdown/0__main/2__pollard-p-minus-1-and-rho-1974.md)
- Тема: Теоретические оценки сложности факторизации с использованием БПФ и описание практического метода p−1 Полларда.
- Summary (EN): Introduces Pollard's p−1 factoring method. Theoretical results: find factor ≤ n^α in O(n^{α/2+δ}) using FFT. Practical p−1 algorithm: if p−1 is L‑smooth, compute a^P and check gcd. Two‑stage version allows one larger prime. Example factors 2^107+2^54+1 with L=199, M=41231. Still used today for numbers with smooth p−1.
- Сводка (RU): Представлен метод факторизации Полларда p−1. Теоретические результаты: нахождение делителя ≤ n^α за O(n^{α/2+δ}) с использованием БПФ. Практический алгоритм p−1: если p−1 L‑гладкое, вычислить a^P и проверить НОД. Двухэтапная версия допускает один больший простой делитель. Пример: делитель числа 2^107+2^54+1 при L=199, M=41231. Метод используется до сих пор для чисел с гладким p−1.
- Ключевые слова: Pollard p−1, integer factorization, smooth numbers, FFT, primality testing, two‑stage method
- ГОСТ: Pollard J. M. Theorems on factorization and primality testing // Mathematical Proceedings of the Cambridge Philosophical Society. – 1974. – Vol. 76, No. 3. – P. 521–528. – DOI: 10.1017/S0305004100049252.

---

### Pollard Rho factorization (Pollard, 1975)
- Файл: [3__pollard-rho-monte-carlo-factorization-1975.md](./markdown/0__main/3__pollard-rho-monte-carlo-factorization-1975.md)
- Тема: Вероятностный алгоритм факторизации («ро» Полларда) с ожидаемой сложностью O(√p) для нахождения простого делителя p.
- Summary (EN): Probabilistic factoring algorithm using iteration of x²−1 modulo n and Floyd's cycle detection. Expected time O(√p) under random mapping assumption. Empirical check on 100 primes near 10⁶ gave r(p)/√p ≈ 1.078. Examples factor 27⁷−3 and 27⁹−3. Still a standard pre‑processor for finding small factors.
- Сводка (RU): Вероятностный алгоритм факторизации с итерацией x²−1 mod n и детекцией цикла Флойда. Ожидаемое время O(√p) в предположении случайности отображения. Эмпирическая проверка на 100 простых вблизи 10⁶ дала r(p)/√p ≈ 1.078. Примеры: факторизация 27⁷−3 и 27⁹−3. До сих пор стандартный этап для поиска малых делителей.
- Ключевые слова: Pollard Rho, integer factorization, Monte Carlo algorithm, cycle detection, Floyd's algorithm, random mapping
- ГОСТ: Pollard J. M. A Monte Carlo method for factorization // BIT Numerical Mathematics. – 1975. – Vol. 15, No. 3. – P. 331–334. – DOI: 10.1007/BF01933667.

---

### ECM practical analysis and MPQS comparison
- Файл: [1__ecm-optimal-parameters-and-qs-comparison-1993.md](./markdown/4__elliptic_curve_method_parameter_selection_ECM/1__ecm-optimal-parameters-and-qs-comparison-1993.md)
- Тема: Оптимальные параметры метода эллиптических кривых (ECM) для факторизации целых чисел и сравнение с квадратичным решетом (MPQS).
- Summary (EN): Numerical integration of Dickman's function gives optimal ECM parameters B₂ ≈ 0.4·K·B₁. For 5–40 digit factors, cost grows as O(p^{1/5}). Bayesian update after failure re-estimates factor size. For 100-digit N, ECM should run <0.2% of MPQS time before switching.
- Сводка (RU): Численное интегрирование функции Дикмана даёт оптимальные параметры ECM: B₂ ≈ 0.4·K·B₁. Для факторов 5–40 цифр стоимость растёт как O(p^{1/5}). Байесовское обновление после неудачи переоценивает размер фактора. Для 100-значных чисел ECM следует запускать на <0.2% времени MPQS перед переключением.
- Ключевые слова: ECM, эллиптические кривые, факторизация, квадратичное решето, MPQS, функция Дикмана, гладкие числа, байесовское обновление
- ГОСТ: Silverman R. D., Wagstaff Jr. S. S. A Practical Analysis of the Elliptic Curve Factoring Algorithm // Mathematics of Computation. – 1993. – Vol. 61, No. 203. – P. 445–462. DOI: 10.1090/S0025-5718-1993-1122078-7

---

### ECM with division polynomials and FFT (Li 2006 thesis)
- Файл: [4__ecm-division-polynomials-fft-thesis-2006.md](./markdown/4__elliptic_curve_method_parameter_selection_ECM/4__ecm-division-polynomials-fft-thesis-2006.md)
- Тема: Практическая реализация ECM с полиномами деления и БПФ для одновременной проверки множества кривых; оптимизация для чисел вида \(s^n \pm 1\).
- Summary (EN): PhD thesis implementing Schnorr's FFT-ECM with implied division polynomials. Complexity \(O(m^2 \ln m)\). Success probability \(1 - (1 - \varepsilon(t))^{m^2/4}\). Optimized for \(s^n \pm 1\): \(O(m^2 \ln m \ln n)\). Found 48-digit factor in 10 days. Open issues: independence assumption, no second step, choice of base \(s\).
- Сводка (RU): Диссертация, реализующая FFT-ECM Шнорра с подразумеваемыми полиномами деления. Сложность \(O(m^2 \ln m)\). Вероятность успеха \(1 - (1 - \varepsilon(t))^{m^2/4}\). Оптимизация для \(s^n \pm 1\): \(O(m^2 \ln m \ln n)\). Найден 48-значный множитель за 10 дней. Открытые вопросы: предположение независимости, отсутствие второго шага, выбор базы \(s\).
- Ключевые слова: ECM, эллиптические кривые, полиномы деления, БПФ, факторизация, Mersenne numbers, Fermat numbers, гладкие числа, множественные кривые
- ГОСТ: Li Z. Elliptic Curve Factoring Method via FFTs with Division Polynomials: PhD dissertation. – West Lafayette: Purdue University, 2006. – 69 p.

---

### Matching AES security with public key systems (Lenstra 2001)
- Файл: [6__matching-aes-security-public-key-sizes-2001.md](./markdown/4__elliptic_curve_method_parameter_selection_ECM/6__matching-aes-security-public-key-sizes-2001.md)
- Тема: Размеры ключей RSA, RSA-MP, DH, LUC, XTR, ECC, эквивалентные по стойкости AES-128/192/256, DES и 3DES, с учётом вычислительной и стоимостной эквивалентности и прогнозов до 2030 г.
- Summary (EN): Determines public key sizes matching symmetric security (56–256 bits). For AES-192 until 2020: RSA 7000–9000 bits, XTR ~1200–1400 bits, ECC ~384–512 bits. Distinguishes computational vs cost equivalence (gap for non-ECC). RSA-MP allows 3–4 factors. Performance tables for encryption/decryption/signing. Small characteristic fields impractically large.
- Сводка (RU): Определены размеры ключей для RSA, XTR, ECC и др., эквивалентные стойкости AES-192 до 2020 г.: RSA — 7000–9000 бит, XTR — 1200–1400 бит, ECC — 384–512 бит. Различие вычислительной и стоимостной эквивалентности. RSA-MP допускает 3–4 фактора. Таблицы производительности. Поля малой характеристики непрактично велики.
- Ключевые слова: AES, RSA, ECC, XTR, LUC, размеры ключей, стойкость, NFS, ECM, факторизация, дискретный логарифм, вычислительная эквивалентность, стоимостная эквивалентность
- ГОСТ: Lenstra A. K. Unbelievable Security: Matching AES Security Using Public Key Systems // Advances in Cryptology — ASIACRYPT 2001. – Berlin, Heidelberg: Springer, 2001. – P. 67–86. DOI: 10.1007/3-540-45682-1_5

---

### Analysis of public-key cryptologic algorithms (Miele 2015)
- Файл: [12__analysis-of-public-key-cryptologic-algorithms-thesis-2015.md](./markdown/4__elliptic_curve_method_parameter_selection_ECM/12__analysis-of-public-key-cryptologic-algorithms-thesis-2015.md)
- Тема: GPU-ускорение NFS, практический анализ Pollard rho с автоморфизмами (род 1–2), FPGA-архитектура для ECDLP, генерация эфемерных ECC-параметров через CM.
- Summary (EN): PhD thesis covering four areas: (1) GPU cofactorization for NFS (50% speedup for 4LP), (2) Pollard rho with automorphisms — actual speedup ~0.79√m, not √m, (3) FPGA many-core design for ECDLP (4.8× faster than prior art), (4) ephemeral ECC parameters via CM with class numbers ≤3 (50ms on smartphone for 128-bit security). Limitations: small CM discriminant, twist-secure generation 20× slower.
- Сводка (RU): Диссертация охватывает: GPU-ускорение пост-решета NFS (+50%), Pollard rho с автоморфизмами — реальный выигрыш ~0.79√m, FPGA-архитектура для ECDLP (в 4.8× быстрее), генерацию эфемерных ECC-параметров через CM (50 мс на смартфоне). Ограничения: малый дискриминант CM, медленная twist-безопасная генерация.
- Ключевые слова: NFS, GPU, ECM, Pollard rho, эллиптические кривые, гиперэллиптические кривые, автоморфизмы, FPGA, ECDLP, комплексное умножение, эфемерные ключи
- ГОСТ: Miele A. On the Analysis of Public-Key Cryptologic Algorithms: PhD dissertation. – Lausanne: EPFL, 2015. – 133 p.

---

### Factoring estimates for 1024-bit RSA (Lenstra et al. 2003)
- Файл: [15__factoring-estimates-1024-bit-rsa-2003.md](./markdown/4__elliptic_curve_method_parameter_selection_ECM/15__factoring-estimates-1024-bit-rsa-2003.md)
- Тема: Оценка параметров факторизации 1024-битного RSA для аппаратного устройства TWIRL; уточнение по результатам численного моделирования и проверки на реальных данных.
- Summary (EN): Evaluated NFS parameters for 1024-bit RSA factoring. Original TWIRL parameters (y≈2.5×10⁸) infeasible — yield too low. Revised parameters (y_r=3.5×10⁹, y_a=2.6×10¹⁰) give 1.9×10¹⁰ relations with manageable filtering. 90nm process reduces cost to ~$1.1M×year. Main uncertainty: large prime matching behavior.
- Сводка (RU): Оценены параметры NFS для факторизации 1024-битного RSA. Оригинальные параметры TWIRL (y≈2.5×10⁸) нереалистичны — слишком малый выход. Уточнённые параметры (y_r=3.5×10⁹, y_a=2.6×10¹⁰) дают 1.9×10¹⁰ соотношений. Переход на 90 нм снижает стоимость до ~$1.1M×год. Основная неопределённость — поведение больших простых в циклах.
- Ключевые слова: RSA, факторизация, NFS, TWIRL, гладкие числа, функция Дикмана, 1024-бит, аппаратная реализация, оценка стоимости
- ГОСТ: Lenstra A., Tromer E., Shamir A., Kortsmit W., Dodson B., Hughes J., Leyland P. Factoring Estimates for a 1024-Bit RSA Modulus // Advances in Cryptology — ASIACRYPT 2003. – Berlin, Heidelberg: Springer, 2003. – P. 55–74. DOI: 10.1007/978-3-540-45146-2_1

---

### Post-quantum RSA (Bernstein et al. 2017)
- Файл: [27__post-quantum-rsa-1-terabyte-keys-2017.md](./markdown/4__elliptic_curve_method_parameter_selection_ECM/27__post-quantum-rsa-1-terabyte-keys-2017.md)
- Тема: Масштабирование RSA до 1-терабайтных ключей (2³¹ простое × 4096 бит) для устойчивости к квантовым атакам; новый квантовый алгоритм GEECM; пакетная генерация простых.
- Summary (EN): Multi-prime RSA with e=3, 2³¹ 4096-bit primes → 1TB public key. Grover-enhanced ECM (GEECM) finds primes up to y² at ECM's cost for y → prime size must be squared. Demonstration: 1TB key generated (4 months on cluster). Encryption feasible (hours), decryption impractical (years). Limitations: decryption bottleneck, trusted key generation, asymptotic GEECM.
- Сводка (RU): Мульти-простое RSA с e=3, 2³¹ простых по 4096 бит → 1-терабайтный открытый ключ. GEECM (ECM с Гровером) находит простые до y² за стоимость ECM для y → размер простых нужно возвести в квадрат. Демонстрация: 1-терабайтный ключ сгенерирован (4 месяца). Шифрование: часы, дешифрование: годы. Ограничения: дешифрование непрактично, генерация ключей требует доверия, GEECM асимптотический.
- Ключевые слова: постквантовая криптография, RSA, GEECM, ECM, Гровер, Шор, мульти-простое RSA, пакетная генерация простых, терабайтные ключи
- ГОСТ: Bernstein D. J., Heninger N., Lou P., Valenta L. Post-quantum RSA // Advances in Cryptology — CRYPTO 2017. – Cham: Springer, 2017. – P. 311–341. DOI: 10.1007/978-3-319-59879-6_18

***

### 20 years of ECM (Zimmermann & Dodson 2006)
- Файл: [9__20-years-of-ecm-2006.md](./markdown/2__ECM_B1_B2_optimization_choice/9__20-years-of-ecm-2006.md)
- Тема: Обзор метода эллиптических кривых (ECM) для факторизации целых чисел спустя 20 лет: алгоритмические улучшения, реализация в GMP-ECM, рекордные множители.
- Summary (EN): Survey of ECM after 20 years. Covers PRAC algorithm with 10 α values, FFT continuation (polynomial arithmetic via Kronecker–Schönhage), block splitting (k=3 optimal), Dickson polynomials, d₁d₂ improvement. Records: 66-digit ECM factor, 58-digit P−1 factor. GMP-ECM 6.0.1 default parameters for 40–65 digit factors. Open problems: stage 1 sequential bottleneck, stage 2 for very large n, stage 3 (two large primes).
- Сводка (RU): Обзор метода эллиптических кривых (ECM) через 20 лет. Описаны: алгоритм PRAC с 10 значениями α, FFT-продолжение (полиномиальная арифметика через трюк Кронекера–Шёнхаге), разбиение на блоки (k=3 оптимально), полиномы Диксона, улучшение d₁d₂. Рекорды: 66-значный множитель ECM, 58-значный множитель P−1. Параметры GMP-ECM 6.0.1 для множителей 40–65 цифр. Открытые проблемы: узкое место stage 1, stage 2 для очень больших n, stage 3 (два больших простых).
- Ключевые слова: ECM, факторизация целых чисел, эллиптические кривые, GMP-ECM, FFT-продолжение, полиномы Диксона, PRAC, рекорды факторизации
- ГОСТ: Zimmermann P., Dodson B. 20 Years of ECM // Algorithmic Number Theory — ANTS VII. – Berlin, Heidelberg: Springer, 2006. – P. 525–542. (LNCS 4076) DOI: 10.1007/11792086_37

---

### Hardware factorization based on ECM (Šimka et al. 2005)
- Файл: [10__hardware-ecm-for-gnfs-cofactorization-2005-simka.md](./markdown/2__ECM_B1_B2_optimization_choice/10__hardware-ecm-for-gnfs-cofactorization-2005-simka.md)
- Тема: Первая аппаратная реализация ECM на FPGA (Xilinx Virtex2000E-6) с управлением от ARM7; параметры B₁=960, B₂=57000, D=30; оценка ASIC для GNFS.
- Summary (EN): First hardware implementation of ECM (FPGA + ARM7). Montgomery form, binary phase 1, B₁=960, B₂=57000, D=30. FPGA (38 MHz): 912 ms phase 1, 1879 ms phase 2 (estimated). ASIC estimate (500 MHz): 55 ms/curve. For GNFS cofactorization: ~6×10⁶ units → 6000 chips, cost <$45k. Phase 2 not fully implemented; ARM-FPGA overhead significant.
- Сводка (RU): Первая аппаратная реализация ECM (FPGA + ARM7). Форма Монтгомери, бинарный stage 1, B₁=960, B₂=57000, D=30. FPGA (38 МГц): stage 1 912 мс, stage 2 1879 мс (оценка). Оценка ASIC (500 МГц): 55 мс/кривую. Для GNFS: ~6·10⁶ блоков → 6000 чипов, стоимость <$45k. Stage 2 не полностью реализован; накладные расходы ARM–FPGA значительны.
- Ключевые слова: ECM, аппаратная реализация, FPGA, ASIC, GNFS, форма Монтгомери, SHARK, ARM7
- ГОСТ: Šimka M., Pelzl J., Kleinjung T., Franke J., Priplata C., Stahlke C., Drutarovský M., Fischer V., Paar C. Hardware Factorization Based on Elliptic Curve Method // 13th Annual IEEE Symposium on Field-Programmable Custom Computing Machines (FCCM 2005). – IEEE, 2005. – P. 107–116. DOI: 10.1109/FCCM.2005.3

---

### Factorization of the tenth Fermat number (Brent 1996)
- Файл: [11__factorization-of-the-tenth-fermat-number-1996.md](./markdown/2__ECM_B1_B2_optimization_choice/11__factorization-of-the-tenth-fermat-number-1996.md)
- Тема: Полная факторизация десятого числа Ферма \(F_{10}\) с помощью метода эллиптических кривых (ECM).
- Summary (EN): Complete factorization of \(F_{10} = 2^{1024}+1\) using ECM with Montgomery form, \(B_1=2\cdot10^6\), birthday paradox continuation. Found 40-digit factor \(p_{40}\); 252-digit cofactor proved prime. Total work ~\(1.4\times10^{11}\) multiplications, ~240 Mips-years. Includes optimal ECM parameter tables and analysis of ECM vs SNFS for Fermat numbers.
- Сводка (RU): Полная факторизация \(F_{10} = 2^{1024}+1\) методом ECM (форма Монтгомери, \(B_1=2\cdot10^6\), продолжение «дня рождения»). Найден 40-значный множитель \(p_{40}\); 252-значный кофактор доказано прост. Объём работы ~\(1.4\times10^{11}\) умножений, ~240 Mips-лет. Приведены таблицы оптимальных параметров ECM и анализ ECM против SNFS для чисел Ферма.
- Ключевые слова: числа Ферма, ECM, эллиптические кривые, факторизация, Монтгомери, день рождения, SNFS, \(F_{10}\), \(F_{11}\)
- ГОСТ: Brent R. P. Factorization of the Tenth Fermat Number // Mathematics of Computation. – 1996. – Vol. 65, No. 213. – P. 429–451. DOI: 10.1090/S0025-5718-96-00710-8

---

### Fast modular arithmetic on Kalray MPPA-256 for ECM (Ishii et al. 2017)
- Файл: [14__fast-modular-arithmetic-on-kalray-mppa-for-ecm-2017.md](./markdown/2__ECM_B1_B2_optimization_choice/14__fast-modular-arithmetic-on-kalray-mppa-for-ecm-2017.md)
- Тема: Энергоэффективная реализация ECM на 256-ядерном процессоре Kalray MPPA-256 для параметров NFS; сравнение с GPU и CPU по пропускной способности и кривым/джоуль.
- Summary (EN): ECM implementation on Kalray MPPA-256 (256 cores, 400 MHz, 16 W). Assembly-coded multiprecision arithmetic (radix 2³², quadratic multiplication, Montgomery reduction). Twisted Edwards curves (a=−1), stage 1 addition chains (B₁ up to 32768), stage 2 BSGS (B₂ up to 360·2¹⁴). Throughput: up to 105k curves/s (192 bits). Energy efficiency: 5–7× better than GPU (GTX580), 20–30× better than CPU. No dedicated squaring; quadratic multiplication only; modulus size fixed at compile time.
- Сводка (RU): Реализация ECM на 256-ядерном Kalray MPPA-256 (400 МГц, 16 Вт). Арифметика многократной точности на ассемблере (радикс 2³², квадратичное умножение, редукция Монтгомери). Скрученные кривые Эдвардса (a=−1), stage 1 — аддитивные цепочки (B₁ до 32768), stage 2 — BSGS (B₂ до 360·2¹⁴). Пропускная способность: до 105k кривых/с (192 бита). Энергоэффективность: в 5–7× лучше GPU, в 20–30× лучше CPU. Нет выделенного возведения в квадрат; умножение только квадратичное; размер модуля фиксируется при компиляции.
- Ключевые слова: ECM, Kalray MPPA-256, многоядерный процессор, многократная точность, метод Монтгомери, NFS, энергоэффективность, скрученные кривые Эдвардса
- ГОСТ: Ishii M., Detrey J., Gaudry P., Inomata A., Fujikawa K. Fast Modular Arithmetic on the Kalray MPPA-256 Processor for an Energy-Efficient Implementation of ECM // IEEE Transactions on Computers. – 2017. – Vol. 66, No. 12. – P. 2019–2030. DOI: 10.1109/TC.2017.2704082

---

### Area-time efficient ECM hardware for NFS (Gaj et al. 2009)
- Файл: [16__area-time-efficient-ecm-hardware-for-nfs-2009.md](./markdown/2__ECM_B1_B2_optimization_choice/16__area-time-efficient-ecm-hardware-for-nfs-2009.md)
- Тема: Аппаратная реализация ECM для NFS (B₁=960, B₂=57000) с двумя умножителями и конвейеризацией; сравнение с Pelzl/Simka и GMP-ECM; анализ производительности на 5 семействах FPGA.
- Summary (EN): FPGA implementation of ECM for NFS cofactorization (200-bit numbers, 40-bit factors). Montgomery form, two parallel multipliers, concurrent P+Q/2P in Phase 1. 9.3× faster Phase 1, 7.3× faster Phase 2 than prior work. Spartan 3: 287 curves/s, 221 curves/s per $100 (17× better than Pentium 4). Virtex II: 430 curves/s. Projection to 1024-bit RSA: 810k Spartan 3E → $29M. Limitations: fixed parameters, no DSP usage, ASIC estimate generic.
- Сводка (RU): Аппаратная реализация ECM для NFS (200-битные числа, 40-битные множители). Форма Монтгомери, два параллельных умножителя, одновременное P+Q и 2P в Phase 1. Ускорение Phase 1 в 9.3×, Phase 2 в 7.3× против Pelzl/Simka. Spartan 3: 287 операций/с, 221 операций/с на $100 (в 17× лучше Pentium 4). Virtex II: 430 операций/с. Для 1024-битного RSA: 810 тыс. Spartan 3E → $29M. Ограничения: фиксированные параметры, DSP не использованы, оценка ASIC по библиотеке.
- Ключевые слова: ECM, аппаратная реализация, FPGA, NFS, факторизация, метод Монтгомери, Spartan, Virtex, GMP-ECM
- ГОСТ: Gaj K., Kwon S., Baier P., Kohlbrenner P., Le H., Khaleeluddin M., Bachimanchi R., Rogawski M. Area-Time Efficient Implementation of the Elliptic Curve Method of Factoring in Reconfigurable Hardware for Application in the Number Field Sieve // IEEE Transactions on Computers. – 2009. – Vol. 58, No. 11. – P. 1485–1500. DOI: 10.1109/TC.2009.131

---

### Factorization of tenth and eleventh Fermat numbers (Brent 1996)
- Файл: [18__factorization-of-fermat-numbers-ecm-1996.md](./markdown/2__ECM_B1_B2_optimization_choice/18__factorization-of-fermat-numbers-ecm-1996.md)
- Тема: Полная факторизация \(F_{10}\) и \(F_{11}\) методом эллиптических кривых (ECM); сравнение платформ (векторные суперкомпьютеры, параллельные системы, DSP-акселератор Dubner Cruncher).
- Summary (EN): Complete factorizations: \(F_{10}=p_8·p_{10}·p_{40}·p_{252}\), \(F_{11}=p_6·p_6·p_{21}·p_{22}·p_{564}\). \(p_{40}\) found after 1.4×10¹¹ multiplications (240 Mips-years). Also found \(p_{27}\) factor of \(F_{13}\) on Dubner Cruncher (493 curves, 47 days). Optimal ECM parameters derived via Dickman function. Full factorization of \(F_{12}\) likely requires quantum computer.
- Сводка (RU): Полные факторизации: \(F_{10}=p_8·p_{10}·p_{40}·p_{252}\), \(F_{11}=p_6·p_6·p_{21}·p_{22}·p_{564}\). \(p_{40}\) найден после 1.4·10¹¹ умножений (240 Mips-лет). Найден также \(p_{27}\) для \(F_{13}\) на Cruncher'е (493 кривые, 47 дней). Оптимальные параметры ECM через функцию Дикмана. Полная факторизация \(F_{12}\) потребует, вероятно, квантового компьютера.
- Ключевые слова: числа Ферма, ECM, факторизация, форма Монтгомери, функция Дикмана, векторные суперкомпьютеры, Dubner Cruncher, GMP-ECM
- ГОСТ: Brent R. P. Factorization of the Tenth and Eleventh Fermat Numbers // Mathematics of Computation. – 1999. – Vol. 68, No. 225. – P. 429–451. DOI: 10.1090/S0025-5718-99-01010-9

---

### HECM using decomposable genus 2 curves and Kummer surfaces (Cosset 2009)
- Файл: [19__hecm-using-decomposable-genus-2-curves-and-kummer-surfaces-2009.md](./markdown/2__ECM_B1_B2_optimization_choice/19__hecm-using-decomposable-genus-2-curves-and-kummer-surfaces-2009.md)
- Тема: Метод гиперэллиптических кривых (HECM) для факторизации с использованием разложимых кривых рода 2 и поверхностей Куммера; сравнение с GMP-ECM.
- Summary (EN): HECM using decomposable genus 2 curves (Jacobian isogenous to E₁×E₂) and Kummer surface arithmetic. One HECM run equals two ECM runs. Parametrization yields small constants (fit in one word) → negligible cost for constant multiplications. For n≥10²⁵⁰, GMP-HECM is 7–11% faster than two GMP-ECM runs. Limitations: higher initialization cost, slower for small n, stage 2 not parallelized, GMP lacks optimized squaring.
- Сводка (RU): HECM с разложимыми кривыми рода 2 (якобиан изогенен произведению двух эллиптических кривых) и арифметикой поверхностей Куммера. Один запуск HECM эквивалентен двум запускам ECM. Параметризация даёт малые константы → умножения на них почти бесплатны. Для n≥10²⁵⁰ GMP-HECM на 7–11% быстрее двух GMP-ECM. Ограничения: дорогая инициализация, медленнее для малых n, stage 2 не распараллелен, в GMP нет оптимизированного возведения в квадрат.
- Ключевые слова: HECM, ECM, факторизация, гиперэллиптические кривые, разложимые кривые, поверхности Куммера, тэта-константы, GMP-ECM
- ГОСТ: Cosset R. HECM: Hyperelliptic Curve Method using decomposable genus 2 curves and Kummer surfaces. – arXiv:0905.2325 [math.NT], 2009. – 18 p.

---

### Cofactorization on GPUs for NFS (Miele et al. 2014)
- Файл: [27__cofactorization-on-gpus-for-nfs-2014.md](./markdown/2__ECM_B1_B2_optimization_choice/27__cofactorization-on-gpus-for-nfs-2014.md)
- Тема: Ускорение кофакторизации в NFS путём переноса всей вычислительной нагрузки на GPU; реализация ECM stage 2 на GPU; интеграция с NFS-сеятелем.
- Summary (EN): Full GPU offload of NFS cofactorization (trial division, Pollard p−1, ECM stages 1+2) on GTX 580. Single thread per (a,b) pair. Montgomery arithmetic (radix 2³²). Twisted Edwards curves (a=−1), stage 2 BSGS with w=210. 27–50% speedup in relations per second. One GPU serves 3–10 quad-core i7 CPUs. Limitations: power not measured; Kepler GPUs no improvement; tested only on 768-bit RSA.
- Сводка (RU): Полный вынос кофакторизации NFS на GPU (пробное деление, Pollard p−1, ECM этапы 1+2) на GTX 580. Один поток на пару (a,b). Арифметика Монтгомери (radix 2³²). Скрученные кривые Эдвардса (a=−1), stage 2 BSGS с w=210. Ускорение сбора отношений на 27–50%. Одна GPU обслуживает 3–10 CPU i7. Ограничения: энергопотребление не измерено; Kepler без улучшений; проверено только на 768-битном RSA.
- Ключевые слова: NFS, кофакторизация, GPU, ECM, CUDA, монтажная арифметика, скрученные кривые Эдвардса, RSA
- ГОСТ: Miele A., Bos J. W., Kleinjung T., Lenstra A. K. Cofactorization on Graphics Processing Units // Cryptographic Hardware and Embedded Systems — CHES 2014. – Berlin, Heidelberg: Springer, 2014. – P. 335–352. DOI: 10.1007/978-3-662-44709-3_19

---

### Area-time efficient hardware architecture for ECM (Pelzl et al. 2005)
- Файл: [29__area-time-efficient-hardware-architecture-for-ecm-2005-pelzl.md](./markdown/2__ECM_B1_B2_optimization_choice/29__area-time-efficient-hardware-architecture-for-ecm-2005-pelzl.md)
- Тема: Первая аппаратная реализация ECM на FPGA (Xilinx Virtex2000E) с управлением от ARM7; параметры B₁=960, B₂=57000, D=30; оценка ASIC для массового параллельного ECM в GNFS.
- Summary (EN): First published hardware implementation of ECM (FPGA + ARM7). Montgomery form, binary method, B₁=960, B₂=57000, D=30. FPGA (38 MHz): 2.7 s/curve. ASIC estimate (500 MHz): 55 ms/curve. For GNFS cofactorization: ~5.9×10⁶ units → 6,000 chips, cost <$45k (negligible). Stage 2 not fully implemented; binary stage1 suboptimal.
- Сводка (RU): Первая опубликованная аппаратная реализация ECM (FPGA + ARM7). Форма Монтгомери, бинарный метод, B₁=960, B₂=57000, D=30. FPGA (38 МГц): 2.7 с/кривую. Оценка ASIC (500 МГц): 55 мс/кривую. Для GNFS: ~5.9·10⁶ блоков → 6,000 чипов, стоимость <$45k (пренебрежимо мала). Stage 2 не полностью реализован; бинарный stage 1 не оптимален.
- Ключевые слова: ECM, аппаратная реализация, FPGA, ASIC, GNFS, форма Монтгомери, SHARK, TWIRL
- ГОСТ: Pelzl J., Šimka M., Kleinjung T., Franke J., Priplata C., Stahlke C., Drutarovský M., Fischer V., Paar C. Area-Time Efficient Hardware Architecture for Factoring Integers with the Elliptic Curve Method // IEE Proceedings — Information Security. – 2005. – Vol. 152, No. 1. – P. 67–78. DOI: 10.1049/ip-ifs:20055018

---

### Optimized ECM on COPACOBANA FPGA cluster (Zimmermann 2009)
- Файл: [32__optimized-ecm-on-fpga-cluster-copacobana-2009.md](./markdown/2__ECM_B1_B2_optimization_choice/32__optimized-ecm-on-fpga-cluster-copacobana-2009.md)
- Тема: Аппаратная реализация ECM (оба этапа) на кластере COPACOBANA (Virtex-4 SX35, 24 ядра на FPGA) с параметрами B₁=960, B₂=57000, D=210; масштабирование от 66 до 236 бит.
- Summary (EN): Full ECM hardware implementation (Phase 1+2) on COPACOBANA cluster. Sequential Montgomery multiplier (3 DSP48s, 200 MHz). Optimized Phase 2 with addition chain precomputation (saving 388 multiplications). Results: 24 cores per FPGA, 9.85 ms/curve → 2,424 curves/s per FPGA (1.86M curves/s on 32-FPGA cluster). Energy efficiency 2× better than GTX 295 GPU. Manual placement required for >19 cores; bit-length fixed at compile time.
- Сводка (RU): Полная аппаратная реализация ECM (этапы 1 и 2) на кластере COPACOBANA. Последовательный умножитель Монтгомери (3 DSP48, 200 МГц). Оптимизированный этап 2 с цепочкой сложений для предвычислений (экономия 388 умножений). Результаты: 24 ядра на FPGA, 9.85 мс/кривую → 2424 кривых/с на FPGA (1.86 млн кривых/с на кластере из 32 FPGA). Энергоэффективность в 2× лучше, чем у GPU GTX 295. Ручное размещение >19 ядер; битность фиксируется при компиляции.
- Ключевые слова: ECM, аппаратная реализация, FPGA, COPACOBANA, Virtex-4, DSP48, метод Монтгомери, GNFS
- ГОСТ: Zimmermann R. Optimized Implementation of the Elliptic Curve Factorization Method on a Highly Parallelized Hardware Cluster: Diploma Thesis. – Bochum: Ruhr University Bochum, 2009. – 101 p.

---

### Prime pairing for smooth group order search (Atnashev & Woltman 2021)
- Файл: [37__prime-pairing-for-smooth-group-order-search-2021.md](./markdown/2__ECM_B1_B2_optimization_choice/37__prime-pairing-for-smooth-group-order-search-2021.md)
- Тема: Улучшение спаривания простых в stage 2 методов P−1, P+1, ECM через перемещаемые простые, графовые паросочетания, нерегулярные расстояния и вторую базу.
- Summary (EN): Improves prime pairing in stage 2 of factorization algorithms. Introduces relocatable primes (multiply by constants coprime to D), graph maximum matching (BFS with subgraph handling), irregular precomputation distances (powers of two), second base (adding D/A). Achieves 99.3% pairing (vs 83.1% for Montgomery) for B₁=9500, B₂=10⁶, D=210, L=8. Implemented in Prefactor and Prime95. Pairings reusable across different numbers. Limitations: matching complexity, second base rarely beneficial for ECM with D<1000.
- Сводка (RU): Улучшение спаривания простых в stage 2 алгоритмов факторизации. Введены перемещаемые простые (умножение на константы), максимальное паросочетание в графе (BFS с обработкой субграфов), нерегулярные расстояния (степени двойки), вторая база (добавление D/A). Достигнуто спаривание 99.3% (против 83.1% у Монтгомери) для B₁=9500, B₂=10⁶, D=210, L=8. Реализовано в Prefactor и Prime95. Спаривания переиспользуются для разных чисел. Ограничения: сложность паросочетания, вторая база редко выгодна для ECM при D<1000.
- Ключевые слова: ECM, P−1, P+1, stage 2, спаривание простых, перемещаемые простые, паросочетание, Монтгомери, Prime95
- ГОСТ: Atnashev P., Woltman G. Prime pairing in algorithms searching for smooth group order. – arXiv preprint, 2021. – 10 p.

***

### Integer factorization using elliptic curves (Brent 1985)
- Файл: [1__integer-factorization-using-elliptic-curves-birthday-paradox-1985.md](./markdown/1__Brent_elliptic_curve_method_factorization/1__integer-factorization-using-elliptic-curves-birthday-paradox-1985.md)
- Тема: Улучшение ECM добавлением второй фазы на основе парадокса дней рождения; теоретическое ускорение O(log p); использование быстрого вычисления полиномов для stage 2.
- Summary (EN): First publication proposing stage 2 for ECM using birthday paradox collision search. Improves Lenstra's one-phase ECM by factor 4–4.5. Success probability μ(α,β) derived from Dickman's function. Fast polynomial evaluation (Karatsuba, Toom–Cook) reduces stage 2 complexity to O(r^{1+ε}). Optimal parameters given. Limitations: heuristic smoothness assumptions; experimental only for p≈10¹².
- Сводка (RU): Первая публикация, предлагающая stage 2 для ECM на основе поиска коллизий (парадокс дней рождения). Ускорение в 4–4.5× по сравнению с однофазным ECM Ленстры. Вероятность успеха μ(α,β) через функцию Дикмана. Быстрое вычисление полиномов (Кацуба, Toom–Cook) снижает сложность stage 2 до O(r^{1+ε}). Приведены оптимальные параметры. Ограничения: эвристические предположения о гладкости; экспериментально только для p≈10¹².
- Ключевые слова: ECM, факторизация, эллиптические кривые, день рождения, stage 2, функция Дикмана, гладкие числа, Ленстра
- ГОСТ: Brent R. P. Some Integer Factorization Algorithms Using Elliptic Curves // Australian Computer Science Communications. – 1986. – Vol. 8. – P. 149–163.

---

### Recent progress and prospects for integer factorisation (Brent 2000)
- Файл: [31__recent-progress-and-prospects-for-integer-factorisation-2000.md](./markdown/1__Brent_elliptic_curve_method_factorization/31__recent-progress-and-prospects-for-integer-factorisation-2000.md)
- Тема: Обзор алгоритмов факторизации (ECM, MPQS, SNFS, GNFS) по состоянию на 2000 год; рекорды; экстраполяция на 1024-битный RSA; параллельная линейная алгебра.
- Summary (EN): Survey of integer factorization algorithms (ECM, MPQS, SNFS, GNFS) as of 2000. Records: ECM 54 digits, GNFS RSA155 (155 digits, 8000 Mips-years). Extrapolation: 1024-bit RSA expected by 2018; ECM 70 digits by 2010. Parallel linear algebra (block Lanczos) communication overhead limits scalability. Pre-elimination can reduce communication at cost of increased storage.
- Сводка (RU): Обзор алгоритмов факторизации (ECM, MPQS, SNFS, GNFS) по состоянию на 2000 год. Рекорды: ECM 54 цифры, GNFS RSA155 (155 цифр, 8000 Mips-лет). Экстраполяция: 1024-битный RSA ожидался к 2018 году; ECM 70 цифр к 2010 году. Параллельная линейная алгебра (block Lanczos) ограничена накладными расходами на связь. Предварительное исключение может уменьшить связь ценой увеличения памяти.
- Ключевые слова: факторизация, ECM, MPQS, GNFS, NFS, RSA, параллельные алгоритмы, Lanczos, решето числового поля
- ГОСТ: Brent R. P. Recent Progress and Prospects for Integer Factorisation Algorithms // Euro-Par 2000 Parallel Processing. – Berlin, Heidelberg: Springer, 2000. – P. 3–22. DOI: 10.1007/3-540-44683-4_1

***

### Speeding Pollard and elliptic curve methods (Montgomery 1987)
- Файл: [1__speeding-pollard-and-elliptic-curve-factoring-methods-1987.md](./markdown/6__Lenstra_elliptic_curve_factorization_1987/1__speeding-pollard-and-elliptic-curve-factoring-methods-1987.md)
- Тема: Ускорение методов Полларда (p−1, ρ) и ECM Ленстры: полиномиальное предобуславливание, улучшенное стандартное продолжение (baby-step giant-step), форма Монтгомери (x:z), параметризация Суямы (делимость порядка на 12), алгоритм PAIR для спаривания простых.
- Summary (EN): Speed improvements for Pollard (p−1, rho) and Lenstra's ECM. Polynomial preconditioning reduces GCD cost (14% speedup for rho). Improved stage 2 using baby-step giant-step (2× faster). Montgomery form (x:z only): addition 6M, doubling 5M, ladder with ~9.3 log₂n multiplications. Suyama parametrization forces group order divisible by 12. Algorithm PAIR pairs primes via residue classes (86% paired for w=1000). Found 33-digit ECM factors. Limitations: heuristic smoothness; ECM stage 2 only outlined.
- Сводка (RU): Ускорение методов Полларда и ECM. Предобуславливание полиномов снижает стоимость НОД (ускорение ρ-метода на 14%). Улучшенное стандартное продолжение (baby-step giant-step) ускоряет stage 2 в 2×. Форма Монтгомери (только x:z): сложение 6M, удвоение 5M, лестница Монтгомери (~9.3 log₂n умножений). Параметризация Суямы обеспечивает делимость порядка группы на 12. Алгоритм PAIR спаривает простые через классы вычетов (86% для w=1000). Найдены 33-значные множители ECM. Ограничения: эвристика гладкости; stage 2 ECM описан схематично.
- Ключевые слова: ECM, факторизация, форма Монтгомери, лестница Монтгомери, stage 2, baby-step giant-step, спаривание простых, p−1, p+1, алгоритм PAIR
- ГОСТ: Montgomery P. L. Speeding the Pollard and Elliptic Curve Methods of Factorization // Mathematics of Computation. – 1987. – Vol. 48, No. 177. – P. 243–264. DOI: 10.1090/S0025-5718-1987-0866113-7

---

### Lenstra factorization method on Edwards curves (Kovalchuk et al. 2018)
- Файл: [7__lenstra-method-on-edwards-curves-factorization-2018.md](./markdown/6__Lenstra_elliptic_curve_factorization_1987/7__lenstra-method-on-edwards-curves-factorization-2018.md)
- Тема: Математическое обоснование адаптации метода Ленстра (ECM) для полных кривых Эдвардса; доказательство корректности; оценка ускорения и вероятности успеха.
- Summary (EN): Rigorous adaptation of Lenstra's ECM from Weierstrass to full Edwards curves. New mathematical results: existence of complementary points (Theorem 2), CRT structure (Theorem 3), non-trivial GCD condition (Theorem 4). Algorithm with unified addition law (10 multiplications per addition vs 16). Speedup at least 1.5×. Experimental evidence: twisted/quadratic Edwards curves give additional 20–30% speedup. Limitations: stage 2 not considered; experiments on small numbers.
- Сводка (RU): Строгая адаптация метода Ленстра (ECM) с кривых Вейерштрасса на полные кривые Эдвардса. Новые математические результаты: существование дополнительных точек (теорема 2), структура через КТО (теорема 3), условие нетривиального НОД (теорема 4). Алгоритм с унифицированным сложением (10 умножений против 16). Ускорение не менее 1.5×. Экспериментально: скрученные/квадратичные кривые дают дополнительные 20–30%. Ограничения: stage 2 не рассмотрен; эксперименты на малых числах.
- Ключевые слова: ECM, факторизация, кривые Эдвардса, метод Ленстра, эллиптические кривые, полные кривые, скрученные кривые Эдвардса, квадратичные кривые
- ГОСТ: Kovalchuk L., Bespalov O., Kuchynska N., Seliukh P., Zhylin A., Tsurkan V. Substantiation of Correctness and Advantages of Lenstra Factorization Method on Edwards Curves // Eastern-European Journal of Enterprise Technologies. – 2018. – Vol. 6, No. 4(96). – P. 2–9. DOI: 10.15587/1729-4061.2018.151090

***

### ECM at work — addition-subtraction chains for GPUs (Bos & Kleinjung 2012)
- Файл: [1__ecm-addition-subtraction-chains-for-memory-constrained-devices-2012.md](./markdown/3__ECM_B1_B2_parameter_selection/1__ecm-addition-subtraction-chains-for-memory-constrained-devices-2012.md)
- Тема: Оптимизация ECM для GPU через предвычисление аддитивно-вычитающих цепочек для фиксированных \(B_1\); снижение памяти до 55×; рекордная пропускная способность.
- Summary (EN): Optimizes ECM for GPUs by precomputing addition-subtraction chains for \(k=\mathrm{lcm}(1,\dots,B_1)\). Two chain types: no-storage (add only input point) and low-storage (few points). Tested \(>10^{12}\) integers for smoothness (40 core-years). Greedy algorithm covers all prime powers. For \(B_1=8192\): memory 10 residues (vs 550), 2% faster. GTX 580: 171k curves/s (\(B_1=960\)), 19.9k curves/s (\(B_1=8192\)) — record. Limitations: precomputation costly (40 core-years), not adaptive, stage 2 not considered.
- Сводка (RU): Оптимизация ECM для GPU через предвычисление аддитивно-вычитающих цепочек для \(k=\mathrm{lcm}(1,\dots,B_1)\). Два типа цепочек: без хранения (только начальная точка) и с низким хранением (несколько точек). Проверено \(>10^{12}\) чисел на гладкость (40 core-лет). Жадный алгоритм покрывает все простые степени. Для \(B_1=8192\): память 10 остатков (против 550), производительность на 2% выше. GTX 580: 171k кривых/с (\(B_1=960\)), 19.9k кривых/с (\(B_1=8192\)) — рекорд. Ограничения: предвычисление дорого (40 core-лет), не адаптивно, stage 2 не рассмотрен.
- Ключевые слова: ECM, GPU, аддитивно-вычитающие цепочки, кривые Эдвардса, кофакторизация, NFS, память, GTX 580
- ГОСТ: Bos J. W., Kleinjung T. ECM at Work // Advances in Cryptology — ASIACRYPT 2012. – Berlin, Heidelberg: Springer, 2012. – P. 467–484. DOI: 10.1007/978-3-642-34961-4_29

---

### High-performance scalable GPU ECM (Wloka et al. 2021)
- Файл: [5__scalable-gpu-ecm-implementation-2021.md](./markdown/3__ECM_B1_B2_parameter_selection/5__scalable-gpu-ecm-implementation-2021.md)
- Тема: Высокопроизводительная GPU-реализация ECM (оба этапа) с поддержкой произвольных параметров; масштабирование до 1024-битного DLP; сравнение w-NAF, FIPS/CIOS, оценка пропускной способности.
- Summary (EN): Scalable GPU implementation of full ECM (stage 1+2) with configurable B₁,B₂, modulus size. a=−1 twisted Edwards curves, w-NAF (w=4) for stage 1, BSGS for stage 2. FIPS modular multiplication fastest on Volta/Turing. RTX 2080 Ti: 214k curves/s (B₁=8192, 192-bit); 2.78k curves/s (B₁=50k, B₂=5M, 448-bit). Open source, multi-GPU. For 1024-bit DLP: individual log from 1 hour (CPU) to minutes (GPU). Limitations: w-NAF suboptimal for small B₁, stage 2 memory-heavy.
- Сводка (RU): Масштабируемая GPU-реализация полного ECM (этапы 1+2) с настраиваемыми B₁,B₂, размером модуля. Кривые Эдвардса a=−1, w-NAF (w=4) для stage 1, BSGS для stage 2. FIPS для умножения на Volta/Turing. RTX 2080 Ti: 214k кривых/с (B₁=8192, 192 бита); 2.78k кривых/с (B₁=50k, B₂=5M, 448 бит). Открытый код, несколько GPU. Для 1024-битного DLP: индивидуальный логарифм с часа на CPU до минут на GPU. Ограничения: w-NAF не оптимален для малых B₁, stage 2 требует много памяти.
- Ключевые слова: ECM, GPU, кривые Эдвардса, w-NAF, BSGS, FIPS, CIOS, RTX 2080 Ti, DLP, NFS
- ГОСТ: Wloka J., Richter-Brockmann J., Güneysu T., Stahlke C., Priplata C., Kleinjung T. A High-Performance and Scalable Implementation of the Elliptic Curve Method on Graphics Processing Units // Topics in Cryptology — CT-RSA 2021. – Cham: Springer, 2021. – P. 306–326. DOI: 10.1007/978-3-030-65411-5_13

***

### JKL-ECM: Hessian curves with torsion for ECM (Heer et al. 2016/2021)
- Файл: [17__jkl-ecm-using-hessian-curves-with-torsion-2021.md](./markdown/3__ECM_B1_B2_parameter_selection/17__jkl-ecm-using-hessian-curves-with-torsion-2021.md)
- Тема: Реализация ECM на скрученных гессиановых кривых из семейств Jeon–Kim–Lee с кручением ℤ/6ℤ⊕ℤ/6ℤ над полем четвёртой степени; использование инъекции кручения (36|#E) и малых параметров для ускорения.
- Summary (EN): ECM implementation using twisted Hessian curves from JKL families with ℤ/6ℤ⊕ℤ/6ℤ torsion over quartic fields. Torsion injection gives guaranteed 36 | #E(𝔽_p) when p splits completely. Generated 4,840 curves with small parameters in 2 weeks. Found 57-digit factor with 1,152 curves (vs 17,899 recommended). Success probability higher than GMP-ECM. Limitations: no assembly optimization (slower), requires special input numbers (x²+3y²), stage 2 memory O(B₂ log B₂).
- Сводка (RU): Реализация ECM на скрученных гессиановых кривых JKL с кручением ℤ/6ℤ⊕ℤ/6ℤ над полями четвёртой степени. Инъекция кручения даёт 36 | #E(𝔽_p) при полном расщеплении p. Сгенерировано 4840 кривых с малыми параметрами за 2 недели. Найден 57-значный множитель за 1152 кривых (против 17 899 в стандартном ECM). Вероятность успеха выше, чем у GMP-ECM. Ограничения: нет ассемблерной оптимизации (медленнее), требуются числа специального вида (x²+3y²), stage 2 требует памяти O(B₂ log B₂).
- Ключевые слова: ECM, гессиановы кривые, кручение, Jeon–Kim–Lee, факторизация, FFT-продолжение, twisted Hessian, JKL
- ГОСТ: Heer H., McGuire G., Robinson O. JKL-ECM: An Implementation of ECM Using Hessian Curves // LMS Journal of Computation and Mathematics. – 2016. – Vol. 19, No. A. – P. 86–102. DOI: 10.1112/S1461157016000231

***

### Faster ECM cofactorization with mixed Edwards‑Montgomery representations
- Файл: [6__faster-cofactorization-ecm-mixed-representations-2019.md](./markdown/5__GMP-ECM_parameter_tuning_optimization/6__faster-cofactorization-ecm-mixed-representations-2019.md)
- Тема: Ускорение ECM для кофакторизации в NFS за счёт комбинации кривых Эдвардса (double‑base chains) и Монтгомери (Lucas chains) с новой операцией ADDₘ.
- Summary (EN): Offline generation of >10¹⁹ double‑base and Lucas chains for fixed B₁. New ADDₘ operation (4M) switches from Edwards to Montgomery. For B₁=8192, stage 1 cost 89572M vs 89991M previous best. Integrated into CADO‑NFS, reduces cofactorization time by 5–10% for RSA‑200/220.
- Сводка (RU): Предвычисление >10¹⁹ double‑base и цепочек Люка для фиксированных B₁. Новая операция ADDₘ (4M) для переключения с кривых Эдвардса на Монтгомери. Для B₁=8192 стоимость стадии 1: 89572M против 89991M у лучшего аналога. Внедрение в CADO‑NFS сокращает время кофакторизации на 5–10% для RSA‑200/220.
- Ключевые слова: ECM, эллиптические кривые, кофакторизация, NFS, twisted Edwards curves, Montgomery curves, double‑base chains, Lucas chains, ADDₘ
- ГОСТ: Bouvier C., Imbert L. Faster cofactorization with ECM using mixed representations // HAL open archive. – 2019. – Preprint. – 23 p.

***

### General Number Field Sieve (Buhler–Lenstra–Pomerance 1993)
- Файл: [3__number-field-sieve-general-integers-1993.md](./markdown/7__elliptic_curve_number_field_sieve_comparison_factorization/3__number-field-sieve-general-integers-1993.md)
- Тема: Распространение NFS на произвольные целые числа с эвристической сложностью \(L_n[1/3, (64/9)^{1/3}+o(1)]\) и преодоление алгебраических препятствий квадратичными характерами.
- Summary (EN): General NFS for arbitrary integers. Base‑m polynomial selection. Sieving on both rational and algebraic sides. Quadratic characters (Adleman) resolve obstructions from class group, units, and non‑maximal order. Heuristic complexity \(L_n[1/3, 1.923]\). Crossover with QS ≈125 digits (1993). Fundamental theoretical foundation for modern integer factorization records.
- Сводка (RU): Общий NFS для произвольных целых. Выбор полинома по основанию \(m\). Просеивание по рациональной и алгебраической сторонам. Квадратичные характеры (Adleman) устраняют препятствия от группы классов, единиц и неглавного порядка. Эвристическая сложность \(L_n[1/3, 1.923]\). Переход с QS ≈125 цифр (1993). Фундаментальная теоретическая основа современных рекордов факторизации.
- Ключевые слова: NFS, факторизация целых чисел, решето числового поля, гладкие числа, квадратичные характеры, алгебраическая теория чисел, сложность \(L_n[1/3]\), RSA
- ГОСТ: Buhler J. P., Lenstra Jr. H. W., Pomerance C. Factoring Integers with the Number Field Sieve // The Development of the Number Field Sieve / Ed. by A. K. Lenstra, H. W. Lenstra Jr. – Berlin, Heidelberg: Springer, 1993. – P. 50–94. – (Lecture Notes in Mathematics; Vol. 1554). – DOI: 10.1007/3-540-57055-4_2.

---

### Аналіз методу факторизації на основі теорії еліптичних кривих (Dermenzhyl & Vostrov, 2019)
- Файл: [5__analysis-of-ecm-probabilistic-nature-2019.md](./markdown/7__elliptic_curve_number_field_sieve_comparison_factorization/5__analysis-of-ecm-probabilistic-nature-2019.md)
- Тема: Огляд методу еліптичних кривих (ECM), його ймовірнісного характеру, субекспоненційної складності та перспектив оптимізації через генератори псевдовипадкових чисел.
- Summary (EN): Survey of ECM focusing on probabilistic nature and subexponential complexity \(L_p[1/2,\sqrt{2}]\). Proposes using PRNGs with distribution matching smooth curve distribution. Highlights Kowalski's analytic number theory results for group structure distribution. Open problems: curve order computation, smooth curve distribution, parameter selection.
- Сводка (RU): Обзор ECM с фокусом на вероятностный характер и субэкспоненциальную сложность \(L_p[1/2,\sqrt{2}]\). Предлагается использовать ГПСЧ с распределением, соответствующим распределению гладких кривых. Отмечены результаты Kowalski по аналитической теории чисел. Открытые проблемы: вычисление порядка кривой, распределение гладких кривых, выбор параметров.
- Ключові слова: еліптична крива, ECM, факторизація, гладкі числа, субекспоненціальна складність, імовірнісний алгоритм, генератор псевдовипадкових чисел, функція Дікмана
- ГОСТ: Дерменжи І. Д., Востров Г. М. Аналіз методу факторизації на основі теорії еліптичних кривих // Electronics and Information Technologies. – 2019. – Вип. 28. – С. 223–233. – ISSN 2221-3805.

---

### Integer factorization algorithms comparison framework (Duta et al., 2016)
- Файл: [7__factorization-algorithms-framework-comparison-2016.md](./markdown/7__elliptic_curve_number_field_sieve_comparison_factorization/7__factorization-algorithms-framework-comparison-2016.md)
- Тема: Реализация и сравнение 14 алгоритмов факторизации (специализированных и общего назначения) для чисел до 50 цифр.
- Summary (EN): Experimental comparison of 14 factorization algorithms on numbers up to 50 digits. Pollard's Rho is fastest for <40 digits (0.009 s). GNFS is fastest general-purpose algorithm (0.267 s for 50 digits). ECM performance improves with input size; becomes competitive beyond 65 digits. Framework provides empirical guidance for algorithm selection.
- Сводка (RU): Экспериментальное сравнение 14 алгоритмов факторизации для чисел до 50 цифр. Pollard's Rho быстрее всех для <40 цифр (0.009 с). GNFS – самый быстрый среди общего назначения (0.267 с для 50 цифр). ECM ускоряется с ростом входного числа; становится конкурентоспособным после 65 цифр. Фреймворк даёт эмпирические рекомендации по выбору алгоритма.
- Ключевые слова: integer factorization, Pollard Rho, ECM, Quadratic Sieve, Number Field Sieve, GNFS, algorithm comparison, special-purpose algorithms, general-purpose algorithms
- ГОСТ: Duta C.-L., Gheorghe L., Tapus N. Framework for Evaluation and Comparison of Integer Factorization Algorithms // [Conference Proceedings]. – 2016. – P. 1–7.

---

### Guide to General Number Field Sieve (Pandey & Pal, 2014)
- Файл: [24__guide-to-general-number-field-sieve-2014.md](./markdown/7__elliptic_curve_number_field_sieve_comparison_factorization/24__guide-to-general-number-field-sieve-2014.md)
- Тема: Обучающее введение в общий метод решета числового поля (GNFS) для факторизации больших целых чисел.
- Summary (EN): Tutorial on GNFS covering difference of squares, smooth numbers, number fields, rational/algebraic/quadratic character factor bases, line and lattice sieving, matrix construction over F₂, and algebraic square root. Complexity L_n[1/3,(64/9)^{1/3}]. Complete example factors 77 = 7·11. Highlights open problems: polynomial selection, parallelization, scaling to RSA‑1024.
- Сводка (RU): Обучающее введение в GNFS: разность квадратов, гладкие числа, числовые поля, факторные базы (рациональная, алгебраическая, квадратичных характеров), линейное и решёточное просеивание, матрица над F₂, алгебраический квадратный корень. Сложность L_n[1/3,(64/9)^{1/3}]. Пример: факторизация 77 = 7·11. Открытые проблемы: выбор полинома, параллелизация, масштабирование до RSA‑1024.
- Ключевые слова: GNFS, integer factorization, number field sieve, smooth numbers, factor base, sieving, LLL, algebraic number theory
- ГОСТ: Pandey G., Pal S. K. A guide to general number field sieve for integer factorization // Investigations in Mathematical Sciences. – 2014. – Vol. 4, No. 2. – P. 83–98.

---

### ECM with Edwards/Hessian curves and quartic torsion (Robinson, 2015)
- Файл: [47__ecm-edwards-hessian-curves-torsion-2015.md](./markdown/7__elliptic_curve_number_field_sieve_comparison_factorization/47__ecm-edwards-hessian-curves-torsion-2015.md)
- Тема: Новая реализация ECM с кривыми Эдвардса/Гессиана, использующая семейства Jeon–Kim–Lee с кручением Z/4Z⊕Z/8Z и Z/6Z⊕Z/6Z над полями четвёртой степени, генерация 700/4840 кривых с малыми параметрами.
- Summary (EN): New ECM implementation using twisted Edwards/Hessian curves from Jeon–Kim–Lee families (torsion Z/4Z⊕Z/8Z, Z/6Z⊕Z/6Z over quartic fields). Generated 700/4840 small‑parameter curves with positive rank. Found 57‑digit prime factor with 1,152 curves at B₁=110M. Effectiveness exceeds GMP‑ECM for primes ≡ 1 mod 3. Hessian addition with small parameters eliminates windowing, reducing memory.
- Сводка (RU): Новая реализация ECM на скрученных кривых Эдвардса/Гессиана из семейств Jeon–Kim–Lee (кручение Z/4Z⊕Z/8Z, Z/6Z⊕Z/6Z над полями четвёртой степени). Сгенерировано 700/4840 кривых с малыми параметрами и положительным рангом. Найден 57‑значный простой делитель за 1152 кривых при B₁=110M. Эффективность превышает GMP‑ECM для простых ≡ 1 mod 3. Сложение на гессиановых кривых с малыми параметрами устраняет windowing, снижая память.
- Ключевые слова: ECM, факторизация, эллиптические кривые, кручение, кривые Эдвардса, гессиановы кривые, Jeon–Kim–Lee, малые параметры, FFT продолжение, GMP
- ГОСТ: Robinson O. M. A New Implementation of the Elliptic Curve Method of Integer Factorization using Edwards and Hessian Curves: Master's thesis / University College Dublin. School of Mathematics and Statistics. – Dublin, 2015. – 92 p.

***

### Survey of integer factorization algorithms (Montgomery, 1994)
- Файл: [1__survey-of-integer-factorization-algorithms-1994.md](./markdown/8__integer_factorization_survey_review_comparison/1__survey-of-integer-factorization-algorithms-1994.md)
- Тема: Всесторонний обзор алгоритмов факторизации от Pollard Rho до NFS с анализом сложности и рекордами 1994 года.
- Summary (EN): Comprehensive survey of integer factorization algorithms (Pollard Rho, P−1, P+1, ECM, CFRAC, QS/MPQS, NFS). Complexity: ECM L_p[1/2,√2]; MPQS L_n[1/2,1]; NFS L_n[1/3,(64/9)^{1/3}]. Records: RSA‑129 (129 digits) by MPQS; 162‑digit Cunningham by NFS. Practical workflow for factoring large integers.
- Сводка (RU): Всесторонний обзор алгоритмов факторизации (Pollard Rho, P±1, ECM, CFRAC, QS/MPQS, NFS). Сложность: ECM L_p[1/2,√2]; MPQS L_n[1/2,1]; NFS L_n[1/3,(64/9)^{1/3}]. Рекорды: RSA‑129 (129 цифр) методом MPQS; 162‑значное число Каннингема методом NFS. Практическое руководство по факторизации больших чисел.
- Ключевые слова: факторизация, Pollard Rho, ECM, квадратичное решето, MPQS, NFS, гладкие числа, сравнение квадратов, RSA, алгоритмы
- ГОСТ: Montgomery P. L. A Survey of Integer Factorization Algorithms. – Amsterdam: CWI, 1994. – 29 p.

---

### Review of integer factorization methods for cryptography (Rabah, 2006)
- Файл: [2__review-of-integer-factorization-for-cryptography-2006.md](./markdown/8__integer_factorization_survey_review_comparison/2__review-of-integer-factorization-for-cryptography-2006.md)
- Тема: Обзор алгоритмов факторизации (Pollard Rho, P−1, ECM, QS/MPQS, NFS) с акцентом на криптоанализ RSA.
- Summary (EN): Comprehensive review of factorization algorithms for RSA cryptanalysis. Covers special‑purpose (Pollard Rho, P−1, ECM) and general‑purpose (QS, MPQS, NFS) methods. Complexity: ECM L_p[1/2,√2], MPQS L_n[1/2,1], GNFS L_n[1/3,(64/9)^{1/3}]. Records: RSA‑129 (1994, MPQS), RSA‑200 (2005, GNFS), 66‑digit ECM factor (2005). Recommends RSA key lengths ≥1024 bits.
- Сводка (RU): Всесторонний обзор алгоритмов факторизации для криптоанализа RSA. Охватывает специализированные (Pollard Rho, P−1, ECM) и общего назначения (QS, MPQS, NFS) методы. Сложность: ECM L_p[1/2,√2], MPQS L_n[1/2,1], GNFS L_n[1/3,(64/9)^{1/3}]. Рекорды: RSA‑129 (1994, MPQS), RSA‑200 (2005, GNFS), 66‑значный делитель ECM (2005). Рекомендует длину RSA‑ключей ≥1024 бит.
- Ключевые слова: RSA, факторизация, ECM, QS, MPQS, NFS, GNFS, Pollard Rho, P−1, криптоанализ, L‑нотация
- ГОСТ: Rabah K. Review of Methods for Integer Factorization Applied to Cryptography // Journal of Applied Sciences. – 2006. – Vol. 6, No. 2. – P. 458–481. – ISSN 1812-5654.

---

### Limitations of evolutionary computation for integer factorization (Mishra et al., 2015)
- Файл: [3__limitations-of-evolutionary-computation-for-factorization-2015.md](./markdown/8__integer_factorization_survey_review_comparison/3__limitations-of-evolutionary-computation-for-factorization-2015.md)
- Тема: Критический анализ эволюционных и био‑инспирированных методов факторизации, объяснение их неспособности масштабироваться до криптографически значимых размеров.
- Summary (EN): Evolutionary and bio‑inspired methods for integer factorization are critically analyzed. Digit‑similarity fitness is deceptive; modular remainder has O(√N) local minima; landscapes provide no selection pressure. Active information injected is negligible vs. blind search. Even N≈10¹⁴ challenges these methods; RSA‑size numbers are impossible. Bio‑inspired approaches cannot replace GNFS/ECM for real cryptography.
- Сводка (RU): Критически проанализированы эволюционные и био‑инспирированные методы факторизации. Фитнес на основе сходства цифр обманчив; функция остатка имеет O(√N) локальных минимумов; ландшафты не дают давления отбора. Вносимая активная информация пренебрежимо мала по сравнению со слепым поиском. Даже N≈10¹⁴ проблематичны; числа размера RSA недостижимы. Био‑инспирированные методы не могут заменить GNFS/ECM в реальной криптографии.
- Ключевые слова: integer factorization, evolutionary computation, genetic algorithm, swarm intelligence, active information, RSA, GNFS, objective function, local minima
- ГОСТ: Mishra M., Gupta V., Chaturvedi U., Shukla K. K., Yampolskiy R. V. A Study on the Limitations of Evolutionary Computation and other Bio-inspired Approaches for Integer Factorization // Procedia Computer Science. – 2015. – Vol. 62. – P. 603–610.

---

### Probabilistic bits for integer factorization (Han et al., 2025)
- Файл: [25__probabilistic-computing-integer-factorization-hbn-sns2-2025.md](./markdown/8__integer_factorization_survey_review_comparison/25__probabilistic-computing-integer-factorization-hbn-sns2-2025.md)
- Тема: Новый вероятностный бит (p‑bit) на 2D материалах h‑BN/SnS₂ с управлением через длительность импульса для обратимых логических вентилей и факторизации целых чисел.
- Summary (EN): Novel p‑bit using h‑BN/SnS₂ 2D materials with stochastic electron trapping/detrapping. Achieves 10⁸ cycles endurance, 3.36 pJ/bit switching energy. Pulse‑width control (10 μs – 10 ms) improves noise immunity. Demonstrates invertible AND/OR/NOT gates and 2‑bit multiplier factorization (N=6→2×3, N=9→3×3). Potential alternative to quantum annealing without cryogenics.
- Сводка (RU): Новый p‑bit на 2D материалах h‑BN/SnS₂ со стохастическим захватом электронов. Выносливость 10⁸ циклов, энергия переключения 3.36 пДж/бит. Управление длительностью импульса (10 мкс – 10 мс) улучшает помехоустойчивость. Продемонстрированы обратимые вентили И, ИЛИ, НЕ и факторизация 2‑битного умножителя (N=6→2×3, N=9→3×3). Потенциальная альтернатива квантовому отжигу без криогеники.
- Ключевые слова: probabilistic computing, p‑bit, integer factorization, invertible logic, 2D materials, h‑BN, SnS₂, interface traps, Ising model
- ГОСТ: Han J.-K., Park J.-Y., Rehman S., Khan M. F., Kim M.-S., Kim S. Highly durable and energy-efficient probabilistic bits based on h-BN/SnS2 interface for integer factorization // InfoMat. – 2025. – Vol. 7, No. 7. – Art. e70018. – DOI: 10.1002/inf2.70018.

---

### Elitist genetic algorithm for integer factorization (Kumari et al., 2024)
- Файл: [33__elitist-genetic-algorithm-for-integer-factorization-2024.md](./markdown/8__integer_factorization_survey_review_comparison/33__elitist-genetic-algorithm-for-integer-factorization-2024.md)
- Тема: Улучшение генетического алгоритма для факторизации целых чисел путём элитизма, удаления дубликатов и снижения кроссовера до 90%; факторизация 22‑значных полупростых чисел.
- Summary (EN): Improved GA for integer factorization with elitism, duplicate removal, and 90% crossover rate. Achieves factorization of 22‑digit semi‑primes (e.g., 3381755902745713031047) in <1 hour, best metaheuristic result to date. Success rate 100% at 11 digits, drops to 3% at 22 digits. Claims parallelizability but not implemented. Not competitive with classical GNFS/ECM for cryptographic sizes.
- Сводка (RU): Улучшенный ГА для факторизации с элитизмом, удалением дубликатов и кроссовером 90%. Достигнута факторизация 22‑значных полупростых чисел (например, 3381755902745713031047) за <1 часа — лучший результат метаэвристической факторизации на сегодня. Успех 100% для 11 цифр, падает до 3% для 22 цифр. Заявляется параллелизуемость, но не реализована. Не конкурентоспособен с классическими GNFS/ECM для криптографических размеров.
- Ключевые слова: integer factorization, genetic algorithm, elitism, RSA cryptanalysis, metaheuristics, semi‑prime
- ГОСТ: Kumari A., Garain U., Bandyopadhyay S., Mishra G., Pal S. K., Bhattacharyya M. RSA Cryptanalysis: An Elitist Genetic Algorithm for Integer Factorization // [Conference Proceedings]. – 2024. – P. 1–5.

---

### Forty years of attacks on RSA (Mumtaz & Ping, 2019)
- Файл: [39__forty-years-of-attacks-on-rsa-survey-2019.md](./markdown/8__integer_factorization_survey_review_comparison/39__forty-years-of-attacks-on-rsa-survey-2019.md)
- Тема: Обзор атак на RSA за 40 лет (1977–2017), включая факторизацию, атаки на слабые экспоненты (Винера, Бона‑Дарфи) и решёточные методы Копперсмита.
- Summary (EN): Survey of RSA attacks over 40 years. Covers integer factorization (GNFS, ECM, QS), elementary attacks (common modulus, blind signature), weak public/private exponent attacks (Wiener: d<N⁰·²⁵, Boneh‑Durfee: d<N⁰·²⁹²), Coppersmith's small root method, Coron's simplification. GNFS complexity L_n[1/3,(64/9)^{1/3}]. RSA‑768 (232 digits) factored in 2010. Well‑implemented RSA remains secure; all attacks exploit parameter or implementation flaws.
- Сводка (RU): Обзор атак на RSA за 40 лет. Охватывает факторизацию (GNFS, ECM, QS), элементарные атаки (общий модуль, слепая подпись), атаки на слабые экспоненты (Винера: d<N⁰·²⁵, Бона‑Дарфи: d<N⁰·²⁹²), метод малых корней Копперсмита, упрощение Корона. Сложность GNFS L_n[1/3,(64/9)^{1/3}]. RSA‑768 (232 цифры) факторизован в 2010. Корректно реализованный RSA остаётся безопасным; все атаки используют ошибки параметров или реализации.
- Ключевые слова: RSA, cryptanalysis, integer factorization, lattice reduction, Coppersmith method, Wiener attack, Boneh‑Durfee attack, GNFS
- ГОСТ: Mumtaz M., Ping L. Forty years of attacks on the RSA cryptosystem: A brief survey // Journal of Discrete Mathematical Sciences and Cryptography. – 2019. – Vol. 22, No. 1. – P. 9–29. – DOI: 10.1080/09720529.2018.1564201.

***

### Beginner's guide to GNFS (Case, 2002)
- Файл: [1__beginners-guide-to-gnfs-2002.md](./markdown/9__factoring_algorithms_RSA_number_field_sieve_quadratic_sieve/1__beginners-guide-to-gnfs-2002.md)
- Тема: Доступное введение в метод решета числового поля общего вида (GNFS) с полным теоретическим объяснением и численным примером факторизации n = 45113 = 197·229.
- Summary (EN): Accessible tutorial on the General Number Field Sieve. Explains difference of squares factorization, construction of polynomial f and integer m, ring ℤ[θ], rational/algebraic factor bases, sieving for smooth (a,b) pairs, matrix construction over GF(2), quadratic characters for square testing, and application of homomorphism to obtain congruence. Complete worked example factors 45113 = 197·229. Conditions for success: #smooth pairs > 1+|ℛ|+|𝒜|+|𝒬|.
- Сводка (RU): Доступное учебное пособие по общему методу решета числового поля. Объясняет метод разности квадратов, построение полинома f и целого m, кольцо ℤ[θ], рациональную и алгебраическую факторные базы, просеивание для поиска гладких пар (a,b), построение матрицы над GF(2), квадратичные характеры для проверки квадратов, применение гомоморфизма для получения сравнения. Полный численный пример: факторизация 45113 = 197·229. Условие успеха: число гладких пар > 1+|ℛ|+|𝒜|+|𝒬|.
- Ключевые слова: GNFS, number field sieve, integer factorization, RSA, smooth numbers, factor base, quadratic characters, sieving, ℤ[θ], difference of squares
- ГОСТ: Case M. A Beginner's Guide To The General Number Field Sieve. – Corvallis, OR: Oregon State University, 2002. – 19 p.

---

### Smooth numbers and the quadratic sieve (Pomerance, 2008)
- Файл: [34__smooth-numbers-and-quadratic-sieve-2008.md](./markdown/9__factoring_algorithms_RSA_number_field_sieve_quadratic_sieve/34__smooth-numbers-and-quadratic-sieve-2008.md)
- Тема: Доступное введение в алгоритм квадратичного решета (QS), роль гладких чисел, эвристический анализ сложности и практические соображения.
- Summary (EN): Gentle introduction to the Quadratic Sieve factoring algorithm. Explains congruence of squares, smooth numbers, the lemma that >π(B) smooth numbers guarantee a square product. Describes sieving for smooth values, optimal parameter choice, heuristic complexity exp((1+o(1))√(log n log log n)). Includes worked example (n=1649). QS is algorithm of choice for 20–120 digit numbers; NFS is faster for larger numbers.
- Сводка (RU): Доступное введение в алгоритм квадратичного решета. Объясняет метод сравнения квадратов, гладкие числа, лемму о том, что >π(B) гладких чисел гарантируют квадратное произведение. Описывает просеивание для поиска гладких значений, оптимальный выбор параметров, эвристическую сложность exp((1+o(1))√(log n log log n)). Включает пример (n=1649). QS – метод выбора для чисел 20–120 цифр; NFS быстрее для бо́льших чисел.
- Ключевые слова: quadratic sieve, QS, гладкие числа, smooth numbers, факторизация, congruence of squares, sieving, Dickman function, эвристическая сложность
- ГОСТ: Pomerance C. Smooth numbers and the quadratic sieve // Surveys in Algorithmic Number Theory / ed. by J. P. Buhler, P. Stevenhagen. – Cambridge University Press, 2008. – P. 69–81. – (MSRI Publications; Vol. 44).

---

### History of integer factorization (Wagstaff, 2013)
- Файл: [45__history-of-integer-factorization-2013.md](./markdown/9__factoring_algorithms_RSA_number_field_sieve_quadratic_sieve/45__history-of-integer-factorization-2013.md)
- Тема: Исторический обзор алгоритмов факторизации от древности до 2013 года, их влияние на RSA и атаки при плохом выборе параметров.
- Summary (EN): Historical survey from trial division to GNFS. Covers Pollard Rho, p−1, CFRAC, QS, ECM, SNFS, GNFS. Complexity: CFRAC L[1/2,√2]; QS L[1/2,1]; ECM L_p[1/2,√2]; SNFS L[1/3,1.526]; GNFS L[1/3,1.923]. Discusses RSA parameter pitfalls (close primes, small d, smooth p±1) and attacks (Wiener, Boneh–Durfee, Coppersmith). Records: RSA‑129, 66‑digit ECM factor, F₉.
- Сводка (RU): Исторический обзор от пробного деления до GNFS. Охватывает Pollard Rho, p−1, CFRAC, QS, ECM, SNFS, GNFS. Сложность: CFRAC L[1/2,√2]; QS L[1/2,1]; ECM L_p[1/2,√2]; SNFS L[1/3,1.526]; GNFS L[1/3,1.923]. Обсуждает проблемы выбора параметров RSA (близкие простые, малые d, гладкие p±1) и атаки (Wiener, Boneh–Durfee, Coppersmith). Рекорды: RSA‑129, 66‑значный делитель ECM, F₉.
- Ключевые слова: integer factorization, history, RSA, Pollard Rho, ECM, QS, GNFS, smooth numbers, continued fractions, Wiener attack, Coppersmith, LLL
- ГОСТ: Wagstaff Jr. S. S. History of integer factorization // The Joy of Factoring. – Providence, RI: American Mathematical Society, 2013. – P. 1–42. – (Student Mathematical Library; Vol. 68). – ISBN 978-0-8218-9002-0.

***

### State of the art in integer factoring (Boudot et al., 2022)
- Файл: [8__state-of-the-art-integer-factoring-2022.md](./markdown/10__RSA_factorization_number_field_sieve_record/8__state-of-the-art-integer-factoring-2022.md)
- Тема: Современное состояние классического криптоанализа факторизации и дискретного логарифмирования (2022): рекорды, прогресс в NFS, оценки для RSA‑1024 и перспективы.
- Summary (EN): Survey of classical cryptanalysis (2022). GNFS for factoring and discrete logarithms. Record: RSA‑250 (829 bits) factored Feb 2020 (2,700 core‑years). 795‑bit DLP computed (3,100 core‑years). 1024‑bit RSA estimated feasible (~500k core‑years). Small‑characteristic DLP has quasi‑polynomial algorithms (binary fields deprecated). ECDLP record: 114 bits. Recommendations: ≥2048‑bit RSA or post‑quantum.
- Сводка (RU): Обзор классического криптоанализа (2022). GNFS для факторизации и дискретных логарифмов. Рекорд: RSA‑250 (829 бит) факторизован в фев. 2020 (2700 core‑лет). DLP для 795‑бит (3100 core‑лет). Оценка RSA‑1024: ~500 000 core‑лет. DLP в полях малой характеристики – квазиполиномиальные алгоритмы (бинарные поля небезопасны). Рекорд ECDLP: 114 бит. Рекомендации: ≥2048 бит для RSA или постквантовые алгоритмы.
- Ключевые слова: RSA, integer factorization, GNFS, discrete logarithm, NFS‑DL, ECDLP, Pollard rho, quantum computing, post‑quantum cryptography
- ГОСТ: Boudot F., Gaudry P., Guillevic A., Heninger N., Thomé E., Zimmermann P. The State of the Art in Integer Factoring and Breaking Public-Key Cryptography // IEEE Security and Privacy Magazine. – 2022. – Vol. 20, No. 2. – P. 80–86. – DOI: 10.1109/MSEC.2022.3141918.

---

### RSA‑768 factorization on heterogeneous computing (Kleinjung et al., 2010)
- Файл: [heterogeneous-computing-rsa-768-factorization-2010.md](./markdown/10__RSA_factorization_number_field_sieve_record/10__heterogeneous-computing-rsa-768-factorization-2010.md)
- Тема: Факторизация RSA‑768 (768 бит, 232 цифры) с использованием гетерогенной вычислительной среды (кластеры, Grid, десктопные гриды) методом решета числового поля.
- Summary (EN): Factored RSA‑768 (768‑bit, 232‑digit) using NFS on heterogeneous infrastructure (clusters, Grid, desktop grids). Sieving: 1500 core‑years, 64B relations. Linear algebra: 119 days (block Wiedemann). 1024‑bit RSA estimated ~500k core‑years. Demonstrates feasibility of large‑scale cryptanalysis; supports NIST recommendation to phase out 1024‑bit RSA.
- Сводка (RU): Факторизация RSA‑768 (768 бит, 232 цифры) методом NFS на гетерогенной инфраструктуре (кластеры, Grid, десктопные гриды). Просеивание: 1500 core‑лет, 64 млрд соотношений. Линейная алгебра: 119 дней (блочный Видерман). Оценка для RSA‑1024: ~500 000 core‑лет. Демонстрация возможности крупномасштабного криптоанализа; подтверждение рекомендации NIST отказаться от RSA‑1024.
- Ключевые слова: RSA, integer factorization, NFS, sieving, block Wiedemann, heterogeneous computing, Grid computing, RSA‑768
- ГОСТ: Kleinjung T., Bos J. W., Lenstra A. K., Osvik D. A., Aoki K., Contini S., Franke J., Thomé E., Jermini P., Thiemard M., Leyland P., Montgomery P. L., Timofeev A., Stockinger H. A heterogeneous computing environment to solve the 768-bit RSA challenge // Designs, Codes and Cryptography. – 2010. – DOI: 10.1007/s10623-010-9455-7.

---

### ECM using Edwards curves (Bernstein et al., 2013)
- Файл: [3__ecm-using-edwards-curves-2013.md](./markdown/11__GMP-ECM/3__ecm-using-edwards-curves-2013.md)
- Тема: Новая реализация ECM (EECM‑MPFQ) на кривых Эдвардса с большим кручением (Z/12Z, Z/2Z×Z/8Z) и малыми параметрами, сравнение с GMP‑ECM.
- Summary (EN): New ECM implementation using twisted Edwards curves in extended coordinates (9M addition). Batch prime processing and signed‑sliding‑window chains reduce multiplications per bit (7.6–8.8 vs ~9). Found 78 (Z/12Z) and 25 (Z/2Z×Z/8Z) curves with small parameters. Z/12Z curve finds 12.16% of 30‑bit primes (B₁=1024) vs 9.01% for Z/4Z. EECM‑MPFQ is faster than GMP‑ECM on 240‑bit numbers.
- Сводка (RU): Новая реализация ECM на скрученных кривых Эдвардса в расширенных координатах (сложение 9M). Пакетная обработка простых и signed‑sliding‑window цепочки снижают число умножений на бит (7.6–8.8 против ~9). Найдено 78 (Z/12Z) и 25 (Z/2Z×Z/8Z) кривых с малыми параметрами. Кривая с Z/12Z находит 12.16% 30‑битных простых (B₁=1024) против 9.01% для Z/4Z. EECM‑MPFQ быстрее GMP‑ECM на 240‑битных числах.
- Ключевые слова: ECM, Edwards curves, twisted Edwards curves, integer factorization, smooth numbers, torsion points, EECM‑MPFQ, GMP‑ECM
- ГОСТ: Bernstein D. J., Birkner P., Lange T., Peters C. ECM using Edwards curves // Mathematics of Computation. – 2013. – Vol. 82, No. 282. – P. 1139–1179. – DOI: 10.1090/S0025-5718-2012-02654-X.

---

### GMP‑ECM implementation (Zimmermann, 2000)
- Файл: [4__gmpecm-implementation-talk-2000.md](./markdown/11__GMP-ECM/4__gmpecm-implementation-talk-2000.md)
- Тема: Реализация метода эллиптических кривых (ECM) в GMP‑ECM: кривые Монтгомери, улучшение Брента‑Суямы, быстрая полиномиальная арифметика, сравнение с Magma и Pari/GP.
- Summary (EN): Presentation of GMP‑ECM, an ECM implementation using Montgomery curves, Brent‑Suyama improvement (e=12,18,30), and fast polynomial arithmetic for stage 2. For 40‑digit factor, B₁=3e6, e=30 gives 3354 curves, 1.93e11 modular multiplications, speedup 1.48 vs e=1. On 500 MHz Alpha, 155‑digit number takes 218 s. GMP‑ECM is ~3× faster than Magma, ~6× faster than Pari/GP.
- Сводка (RU): Презентация GMP‑ECM – реализации ECM на кривых Монтгомери с улучшением Брента‑Суямы (e=12,18,30) и быстрой полиномиальной арифметикой для стадии 2. Для 40‑значного делителя, B₁=3e6, e=30: 3354 кривых, 1.93e11 умножений, ускорение 1.48. На 500 MHz Alpha, 155‑значное число: 218 с. GMP‑ECM примерно в 3× быстрее Magma, в 6× быстрее Pari/GP.
- Ключевые слова: ECM, GMP‑ECM, Montgomery curves, Brent‑Suyama, polynomial multiplication, integer factorization, stage 2
- ГОСТ: Zimmermann P. GMP-ECM: yet another implementation of the Elliptic Curve Method (or how to find a 40-digit prime factor within 2·10¹¹ modular multiplications). – 2000. – Conference presentation.

---

### Experimental comparison of factoring algorithms (Milan, 2010)
- Файл: [26__experimental-comparison-factoring-algorithms-2010.md](./markdown/11__GMP-ECM/26__experimental-comparison-factoring-algorithms-2010.md)
- Тема: Экспериментальное сравнение алгоритмов факторизации (SQUFOF, McKee, ECM, CFRAC, SIQS) для чисел 45–200 бит с рекомендациями по выбору.
- Summary (EN): Experimental comparison of SQUFOF, McKee's Fermat, ECM, CFRAC, and SIQS on 45–200 bit composites (product of two equal primes). SQUFOF fastest ≤60 bits. SIQS fastest for 70–200 bits (200‑bit composite ~160 s on 2009 Opteron). CFRAC slower than SIQS across all sizes. Batch smoothness detection (Bernstein) speeds CFRAC but still slower. McKee's method not competitive. Practical recommendations for algorithm selection based on input size.
- Сводка (RU): Экспериментальное сравнение SQUFOF, McKee, ECM, CFRAC и SIQS на числах 45–200 бит (произведение двух равных простых). SQUFOF быстрее всего до 60 бит. SIQS быстрее всего для 70–200 бит (200‑битное число ~160 с на Opteron 2009). CFRAC медленнее SIQS во всём диапазоне. Пакетное обнаружение гладкости (Бернстайн) ускоряет CFRAC, но всё равно медленнее. Метод McKee неконкурентоспособен. Практические рекомендации по выбору алгоритма в зависимости от размера числа.
- Ключевые слова: integer factorization, SQUFOF, ECM, CFRAC, SIQS, quadratic sieve, batch smoothness, experimental comparison
- ГОСТ: Milan J. Experimental comparison of integer factoring algorithms for medium-sized composites. – Palaiseau: LIX, École Polytechnique, 2010. – 16 p.

---

### FFT continuation for P±1 (Montgomery & Kruppa, 2008)
- Файл: [fft-extension-to-p-minus-1-and-p-plus-1-2008.md](./markdown/11__GMP-ECM/27__fft-extension-to-p-minus-1-and-p-plus-1-2008.md)
- Тема: Эффективная по памяти FFT‑реализация стадии 2 для методов P−1 и P+1 с B₂ до 10¹⁶, включая рекордные факторы.
- Summary (EN): Space‑efficient FFT stage 2 for Pollard P−1 and Williams P+1. Uses NTT, reciprocal Laurent polynomials, weighted convolutions. ℓ_max = 2²³ on 4 GB; ℓ_max = 2²⁶ on 32 GB. Speedup ~20× over previous product‑tree implementation. Records: 60‑digit P+1 factor of L₂₃₆₆; 17‑digit q for 24¹⁴²+1. Integrated into GMP‑ECM.
- Сводка (RU): Эффективная по памяти FFT‑стадия 2 для P−1 и P+1. Использует NTT, взаимные многочлены Лорана, взвешенные свёртки. ℓ_max = 2²³ на 4 ГБ; ℓ_max = 2²⁶ на 32 ГБ. Ускорение ~20× по сравнению с предыдущей реализацией. Рекорды: 60‑значный P+1 делитель L₂₃₆₆; 17‑значный q для 24¹⁴²+1. Внедрено в GMP‑ECM.
- Ключевые слова: P−1, P+1, integer factorization, FFT, NTT, reciprocal polynomials, multipoint evaluation, geometric progression, GMP‑ECM
- ГОСТ: Montgomery P. L., Kruppa A. FFT continuation of P-1 and P+1 factorization algorithms. – 2008. – 20 p. – (HAL preprint).

---

### Alternative sieving strategies for NFS (Bouillaguet et al., 2023)
- Файл: [2__alternative-sieving-strategies-for-nfs-2023.md](./markdown/12__ECM-other/2__alternative-sieving-strategies-for-nfs-2023.md)
- Тема: Ускорение сбора соотношений в NFS путём комбинирования просеивания и пакетного алгоритма Бернстайна для очень малых простых на одной стороне.
- Summary (EN): Improves NFS relation collection by combining sieving (medium/large primes) with Bernstein's batch smooth part algorithm (extra‑small primes) on the same side. Analyzes RSA‑250 relations (8.4G) to model prime occurrence (probability ~1/p^α, α≈2.4–2.5). Modifies Cado‑NFS to skip sieving primes <2¹⁷, recovers them via batch algorithm. Achieves 90% relations in 82% time locally, projected overall speedup ≈5%. Practical demonstration on record‑sized data.
- Сводка (RU): Ускорение сбора соотношений в NFS комбинированием просеивания (средние/большие простые) с пакетным алгоритмом Бернстайна для очень малых простых на той же стороне. Анализ 8.4 млрд соотношений RSA‑250: вероятность появления простых ~1/p^α, α≈2.4–2.5. Модификация Cado‑NFS: отключение просеивания для простых <2¹⁷, восстановление через пакетный алгоритм. Локальное ускорение: 90% соотношений за 82% времени, прогнозируемое общее ускорение ≈5%. Экспериментальная проверка на данных рекордного размера.
- Ключевые слова: NFS, number field sieve, sieving, batch smooth part, Bernstein algorithm, RSA‑250, integer factorization, Cado‑NFS
- ГОСТ: Bouillaguet C., Fleury A., Fouque P.-A., Kirchner P. We are on the same side. Alternative sieving strategies for the number field sieve // Advances in Cryptology – ASIACRYPT 2023 / ed. by J. Guo, R. Steinfeld. – Cham: Springer, 2023. – P. 138–166. – (LNCS; Vol. 14439). – DOI: 10.1007/978-981-99-8730-6_5.

---

### ECM on GPUs (2020) – high-throughput implementation
- Файл: [8__ecm-on-gpus-high-throughput-implementation-2020.md](./markdown/12__ECM-other/8__ecm-on-gpus-high-throughput-implementation-2020.md)
- Тема: Высокопроизводительная реализация метода эллиптических кривых (ECM) на GPU с поддержкой произвольных параметров и нескольких устройств.
- Summary (EN): GPU implementation of ECM using Twisted Edwards curves (a=−1), w-NAF scalar multiplication, and FIPS Montgomery multiplication. Achieves 214k trials/sec (stage 1, B₁=8192, 192-bit) on RTX 2080 Ti. Supports arbitrary B₁/B₂ and multi-GPU scaling. Open source. Reduces 768-bit DLP individual log latency from 3 to 2 minutes.
- Сводка (RU): Реализация ECM на GPU с использованием скрученных кривых Эдвардса (a=−1), w-NAF и умножения Монтгомери (FIPS). Достигнуто 214 тыс. попыток/сек (этап 1, B₁=8192, 192 бит) на RTX 2080 Ti. Поддержка произвольных B₁/B₂ и нескольких GPU. Open source. Сокращение времени индивидуального логарифма для 768 бит с 3 до 2 минут.
- Ключевые слова: ECM, GPU, факторизация, эллиптические кривые, GNFS, дискретный логарифм, Twisted Edwards, Montgomery умножение, PTX, CUDA
- ГОСТ: Wloka J., Richter-Brockmann J., Stahlke C., Priplata C., Kleinjung T., Güneysu T. Revisiting ECM on GPUs. – 2020. – DOI отсутствует.

---

### Twisted Edwards curves for ECM (2010)
- Файл: [12__twisted-edwards-curves-for-ecm-2010.md](./markdown/12__ECM-other/12__twisted-edwards-curves-for-ecm-2010.md)
- Тема: Построение скрученных кривых Эдвардса с a=−1 и торсионными группами Z/2×Z/4, Z/8, Z/6 для улучшения эффективности ECM.
- Summary (EN): Constructs a=−1 twisted Edwards curves with Z/6 torsion that outperform prior Z/12 curves. Best curve: −x² + y² = 1 − (6517/196608)·x²y². Finds 4% more primes and runs 4% faster due to 8M addition. Tested on 15–26 bit primes. Provides explicit parametrizations and infinite families.
- Сводка (RU): Построены скрученные кривые Эдвардса с a=−1 и торсионной группой Z/6, превосходящие предыдущие кривые с Z/12. Лучшая кривая: −x² + y² = 1 − (6517/196608)·x²y². Находит на 4% больше простых чисел и работает на 4% быстрее за счёт сложения за 8M. Протестировано на 15–26-битных простых числах. Даны явные параметризации и бесконечные семейства.
- Ключевые слова: ECM, факторизация, эллиптические кривые, скрученные кривые Эдвардса, торсионная группа, Suyama, Edwards curves
- ГОСТ: Bernstein D. J., Birkner P., Lange T. Twisted Edwards Curves for the Elliptic Curve Method of Factorization // IACR Cryptology ePrint Archive. – 2010. – Report 2010/367.

---

### FPGA ECM on COPACOBANA (2010)
- Файл: [17__fpga-ecm-implementation-virtex4-2010.md](./fpga-ecm-implementation-virtex4-2010.md)
- Тема: Высокопроизводительная реализация метода эллиптических кривых (ECM) на FPGA Virtex-4 в составе кластера COPACOBANA для факторизации чисел 66–236 бит.
- Summary (EN): FPGA implementation of ECM with 24 cores per Virtex-4 SX35 using DSP-based Montgomery multiplication (Orup's method). Achieves 2,424 factorizations/sec (151-bit, B₁=960, B₂=57,000). 37× better cost-performance than prior Virtex-4 designs. Scales to 310k factorizations/sec on 128-FPGA COPACOBANA cluster.
- Сводка (RU): Реализация ECM на FPGA с 24 ядрами на Virtex-4 SX35 с использованием DSP-блоков для умножения Монтгомери (метод Orup). Достигнуто 2 424 факторизации/сек (151 бит, B₁=960, B₂=57 000). Соотношение цена/производительность лучше в 37 раз по сравнению с аналогами. Масштабирование до 310 тыс. факторизаций/сек на 128 FPGA COPACOBANA.
- Ключевые слова: ECM, факторизация, FPGA, COPACOBANA, Montgomery умножение, DSP, Virtex-4, NFS
- ГОСТ: Zimmermann R., Güneysu T., Paar C. High-Performance Integer Factoring with Reconfigurable Devices // 2010 International Conference on Field Programmable Logic and Applications (FPL). – IEEE, 2010. – P. 87–92. (DOI отсутствует)

---

### Differential Evolution algorithm overview (2005)
- Файл: [53__differential-evolution-overview-and-analysis-2005.md](./differential-evolution-overview-and-analysis-2005.md)
- Тема: Подробный обзор алгоритма дифференциальной эволюции (DE): структура популяции, операторы мутации и кроссовера, механизмы селекции, теоретический анализ и практические рекомендации по выбору параметров.
- Summary (EN): Comprehensive overview of Differential Evolution (DE/rand/1/bin). Covers population initialization, differential mutation with scale factor F, exponential/binomial crossover with probability Cr, one-to-one selection. Analyzes critical F values, rotation invariance, degenerate index combinations. Phase portraits show successful strategies cluster on mutation/recombination axes. Recommendations: F∈[0.5,0.9], Cr low for separable functions, high for epistatic, Np≈5–10×D. Rotation invariance only at Cr=1.
- Сводка (RU): Полный обзор алгоритма дифференциальной эволюции (DE/rand/1/bin). Описаны инициализация популяции, дифференциальная мутация с масштабным коэффициентом F, экспоненциальный/биномиальный кроссовер с вероятностью Cr, попарная селекция. Проанализированы критические значения F, инвариантность к повороту, вырожденные комбинации индексов. Фазовые портреты показывают кластеризацию успешных стратегий на осях мутации или рекомбинации. Рекомендации: F∈[0.5,0.9], Cr мал для сепарабельных функций / высок для эпистатических, Np≈5–10×D. Инвариантность к повороту только при Cr=1.
- Ключевые слова: дифференциальная эволюция, DE, глобальная оптимизация, мутация, кроссовер, селекция, параметры управления, эволюционные алгоритмы
- ГОСТ: Price K. V. The Differential Evolution Algorithm // Differential Evolution: A Practical Approach to Global Optimization. – Springer, 2005. – Chapter 2. – P. 37–134. (DOI отсутствует)

---

### Recent Advances in Bayesian Optimization (2023 survey)
- Файл: [54__recent-advances-in-bayesian-optimization-2023.md](./recent-advances-in-bayesian-optimization-2023.md)
- Тема: Всесторонний обзор современных достижений байесовской оптимизации (BO) на основе гауссовских процессов, включая высокоразмерную, комбинаторную, робастную, с ограничениями, многоцелевую, многозадачную, многогочную оптимизацию, перенос знаний, пакетную BO и новые направления (федеративная оптимизация, справедливость, динамические задачи).
- Summary (EN): Comprehensive survey of GP-based Bayesian optimization across nine categories: high-dimensional, combinatorial, noisy/robust, constrained, multi-objective, multi-task, multi-fidelity, transfer learning, and parallel BO. Covers acquisition functions (PI, EI, UCB, KG, ES/PES, MES) and surrogate models. Identifies emerging challenges: federated BO, fairness, dynamic optimization, heterogeneous evaluations, non-stationarity, negative transfer. No empirical comparison; qualitative analysis.
- Сводка (RU): Полный обзор байесовской оптимизации на основе гауссовских процессов по девяти категориям: высокоразмерная, комбинаторная, робастная, с ограничениями, многоцелевая, многозадачная, многогочная, с переносом знаний и пакетная BO. Описаны функции приобретения (PI, EI, UCB, KG, ES/PES, MES) и суррогатные модели. Выделены новые вызовы: федеративная BO, справедливость, динамическая оптимизация, гетерогенные вычисления, нестационарность, негативный перенос. Качественный анализ без эмпирического сравнения.
- Ключевые слова: байесовская оптимизация, BO, гауссовский процесс, GP, функция приобретения, высокоразмерная оптимизация, многоцелевая оптимизация, MOP, многогочная оптимизация, MFO, перенос обучения, пакетная оптимизация, федеративная оптимизация
- ГОСТ: Wang X., Jin Y., Schmitt S., Olhofer M. Recent Advances in Bayesian Optimization // ACM Computing Surveys. – 2023. – Vol. 55, No. 13s. – Article 287. DOI: 10.1145/3582078.

---

### Random Search for Hyper-Parameter Optimization (2012)
- Файл: [55__random-search-for-hyperparameter-optimization-2012.md](./random-search-for-hyperparameter-optimization-2012.md)
- Тема: Сравнение эффективности случайного поиска и поиска по сетке для оптимизации гиперпараметров алгоритмов машинного обучения.
- Summary (EN): Demonstrates that random search is more efficient than grid search for hyper-parameter optimization due to low effective dimensionality of response surfaces. Neural network experiments: 8 random trials match grid search with ~100 trials. DBN experiments (32 hyper-parameters): random search competitive with expert manual+grid search on 5/7 datasets. Recommends random search as baseline for adaptive hyper-parameter optimization.
- Сводка (RU): Показано, что случайный поиск эффективнее поиска по сетке для оптимизации гиперпараметров из-за низкой эффективной размерности функций отклика. Эксперименты с нейросетями: 8 случайных попыток соответствуют поиску по сетке из ~100 попыток. Эксперименты с DBN (32 гиперпараметра): случайный поиск конкурентоспособен с экспертным ручным+сеточным поиском на 5 из 7 датасетов. Рекомендуется использовать случайный поиск как базовый уровень для адаптивных методов оптимизации гиперпараметров.
- Ключевые слова: гиперпараметры, оптимизация, случайный поиск, поиск по сетке, машинное обучение, нейронные сети, глубокое обучение, эффективная размерность
- ГОСТ: Bergstra J., Bengio Y. Random Search for Hyper-Parameter Optimization // Journal of Machine Learning Research. – 2012. – Vol. 13. – P. 281–305.

---

### Efficient Global Optimization (EGO) – 1998
- Файл: [56__efficient-global-optimization-expensive-functions-1998.md](./efficient-global-optimization-expensive-functions-1998.md)
- Тема: Эффективная глобальная оптимизация дорогих черных ящиков с использованием гауссовских процессов (DACE) и критерия ожидаемого улучшения (Expected Improvement).
- Summary (EN): Introduces EGO algorithm for expensive black-box optimization using DACE Gaussian process models. Expected improvement criterion E[I(x)] = (f_min−ŷ)Φ(·) + s·φ(·) balances exploration and exploitation. Solves 2D problems in ~30 evaluations, 3D in ~35, 6D in ~84. Provides cross-validation diagnostics, variance decomposition for visualization, and a credible stopping rule.
- Сводка (RU): Представлен алгоритм EGO для оптимизации дорогих черных ящиков с использованием гауссовских процессов DACE. Критерий ожидаемого улучшения E[I(x)] = (f_min−ŷ)Φ(·) + s·φ(·) балансирует исследование и эксплуатацию. Решает 2D задачи за ~30 вычислений, 3D за ~35, 6D за ~84. Предоставляет диагностику кросс-валидации, декомпозицию дисперсии для визуализации и правило остановки.
- Ключевые слова: EGO, эффективная глобальная оптимизация, DACE, гауссовский процесс, кригинг, ожидаемое улучшение, Expected Improvement, дорогие вычисления, оптимизация черного ящика
- ГОСТ: Jones D. R., Schonlau M., Welch W. J. Efficient Global Optimization of Expensive Black-Box Functions // Journal of Global Optimization. – 1998. – Vol. 13. – P. 455–492.

---

### ParamILS: Automatic Algorithm Configuration (2009)
- Файл: [57__paramils-automatic-algorithm-configuration-2009.md](./paramils-automatic-algorithm-configuration-2009.md)
- Тема: Автоматическая конфигурация параметров алгоритмов (включая категориальные) с помощью итеративного локального поиска и адаптивного отсечения.
- Summary (EN): ParamILS framework for automatic algorithm configuration using iterated local search with one-exchange neighbourhood. Includes BasicILS (fixed N evaluations) and FocusedILS (adaptive N with domination criterion). Adaptive capping prunes poor configurations early. Achieves speedups over defaults up to 3540× on SAT solvers. First automatic configuration of CPLEX (up to 23× speedup). Open source.
- Сводка (RU): Фреймворк ParamILS для автоматической конфигурации алгоритмов с использованием итеративного локального поиска с однообменной окрестностью. Включает BasicILS (фиксированное N оценок) и FocusedILS (адаптивное N с критерием доминирования). Адаптивное отсечение досрочно прекращает оценку плохих конфигураций. Достигнуто ускорение относительно значений по умолчанию до 3540× для SAT-солверов. Первая автоматическая конфигурация CPLEX (ускорение до 23×). Открытый код.
- Ключевые слова: конфигурация алгоритмов, автоматическая настройка параметров, итеративный локальный поиск, ParamILS, SAT, CPLEX, адаптивное отсечение
- ГОСТ: Hutter F., Hoos H. H., Leyton-Brown K., Stützle T. ParamILS: An Automatic Algorithm Configuration Framework // Journal of Artificial Intelligence Research. – 2009. – Vol. 36. – P. 267–306.

---

### Practical Bayesian Optimization (NIPS 2012)
- Файл: [58__practical-bayesian-optimization-ml-algorithms-2012.md](./practical-bayesian-optimization-ml-algorithms-2012.md)
- Тема: Практические методы байесовской оптимизации для настройки гиперпараметров алгоритмов машинного обучения с учётом ковариации, времени вычислений и параллельных экспериментов.
- Summary (EN): Bayesian optimization for hyperparameter tuning using GP with Matérn 5/2 kernel, fully Bayesian marginalization of hyperparameters (slice sampling), expected improvement acquisition, cost-aware EI per second, and Monte Carlo parallel acquisition. Outperforms grid/random search on LDA (15 vs 288 evaluations), protein motif finding (40 vs 1,400), and CIFAR-10 convnets (14.98% vs expert 18% error). First BO to surpass human expert on deep learning.
- Сводка (RU): Байесовская оптимизация гиперпараметров с использованием GP и ядра Матерна 5/2, полным байесовским маргинализованием гиперпараметров (срезочная выборка), критерием ожидаемого улучшения, стоимость-ориентированным EI в секунду и параллельным Monte Carlo acquisition. Превосходит поиск по сетке/случайный поиск на LDA (15 vs 288 вычислений), поиске мотивов в белках (40 vs 1,400) и свёрточных сетях на CIFAR-10 (14.98% vs экспертные 18%). Первая BO, превзошедшая человека-эксперта в глубоком обучении.
- Ключевые слова: байесовская оптимизация, гауссовский процесс, гиперпараметры, настройка, ожидаемое улучшение, ядро Матерна, параллельная оптимизация, стоимость-ориентированная оптимизация, глубокое обучение, CIFAR-10
- ГОСТ: Snoek J., Larochelle H., Adams R. P. Practical Bayesian Optimization of Machine Learning Algorithms // Advances in Neural Information Processing Systems 25 (NIPS 2012). – 2012. – P. 2951–2959.

---

### Particle Swarm Optimization (1995)
- Файл: [59__particle-swarm-optimization-introduction-1995.md](./particle-swarm-optimization-introduction-1995.md)
- Тема: Введение метода оптимизации роя частиц (PSO) для непрерывных нелинейных функций, вдохновлённого социальным поведением птичьих стай и косяков рыб.
- Summary (EN): Introduces Particle Swarm Optimization (PSO) for continuous nonlinear functions. Particles fly through D-dimensional space, adjusting velocities toward personal best (pbest) and global best (gbest) with stochastic acceleration. Trains XOR NN in ~31 iterations; Fisher Iris in 284 epochs; outperforms backpropagation on EEG (92% vs 89%). Extremely simple, computationally inexpensive. No convergence proofs; constant factor (2) heuristic.
- Сводка (RU): Представлен метод оптимизации роя частиц (PSO) для непрерывных нелинейных функций. Частицы движутся в многомерном пространстве, корректируя скорости в сторону личного лучшего (pbest) и глобального лучшего (gbest) со стохастическим ускорением. Обучение нейросети XOR за ~31 итерацию; Iris Фишера за 284 эпохи;优于 обратного распространения на ЭЭГ (92% против 89%). Чрезвычайно прост, вычислительно дёшев. Отсутствуют доказательства сходимости; константа (2) эвристическая.
- Ключевые слова: PSO, оптимизация роя частиц, swarm intelligence, нейронные сети, глобальная оптимизация, эволюционные вычисления, рой, пунктир
- ГОСТ: Eberhart R. C., Kennedy J. Particle Swarm Optimization // Proceedings of IEEE International Conference on Neural Networks. – 1995. – Vol. 4. – P. 1942–1948.

---

### Differential Evolution (1997)
- Файл: [60__differential-evolution-global-optimization-1997.md](./differential-evolution-global-optimization-1997.md)
- Тема: Представление метода дифференциальной эволюции (DE) для глобальной оптимизации непрерывных функций с демонстрацией превосходства над методами отжига, эволюционными алгоритмами и стохастическими дифференциальными уравнениями.
- Summary (EN): Introduces Differential Evolution (DE/rand/1/bin): population of NP vectors, mutation using weighted difference of two vectors, binomial crossover, greedy selection. Outperforms annealing (ASA, ANM), evolutionary algorithms (BGA, EASY), and SDE on 29+ test functions. Finds all minima across 3 testbeds. Simple (<30 lines C), robust parameters (NP, F, CR). No convergence proof; scaling >100 parameters unknown.
- Сводка (RU): Представлен метод дифференциальной эволюции (DE/rand/1/bin): популяция из NP векторов, мутация с использованием взвешенной разности двух векторов, биномиальный кроссовер, жадная селекция. Превосходит методы отжига (ASA, ANM), эволюционные алгоритмы (BGA, EASY) и SDE на 29+ тестовых функциях. Находит все минимумы в 3 тестовых наборах. Простой (<30 строк C), робастные параметры (NP, F, CR). Нет доказательства сходимости; масштабирование для >100 параметров неизвестно.
- Ключевые слова: дифференциальная эволюция, DE, глобальная оптимизация, эволюционные алгоритмы, мутация, кроссовер, непрерывная оптимизация
- ГОСТ: Storn R., Price K. Differential Evolution - A Simple and Efficient Heuristic for Global Optimization over Continuous Spaces // Journal of Global Optimization. – 1997. – Vol. 11. – P. 341–359.

---

### irace: Iterated Racing for Algorithm Configuration (2016)
- Файл: [61__irace-iterated-racing-algorithm-configuration-2016.md](./irace-iterated-racing-algorithm-configuration-2016.md)
- Тема: Пакет irace для автоматической конфигурации алгоритмов методом итеративных гонок (iterated racing) с поддержкой смешанных и условных параметров.
- Summary (EN): R package for automatic algorithm configuration using iterated racing (I/F-Race). Supports categorical, numerical, ordinal, conditional parameters. Sampling via truncated normal (numerical) / discrete (categorical). Selection via Friedman or t-test with sequential elimination. Extensions: soft-restart (avoid premature convergence), elitist racing (preserve best configs), parallel evaluation. Outperforms defaults on ACOTSP, MOACO, SPEAR. Used in optimization, ML, robotics. Open source.
- Сводка (RU): R-пакет для автоматической конфигурации алгоритмов методом итеративных гонок (I/F-Race). Поддерживает категориальные, числовые, порядковые и условные параметры. Выборка через усечённое нормальное (числовые) / дискретное (категориальные) распределения. Отбор через критерий Фридмана или t-тест с последовательным исключением. Расширения: soft-restart (предотвращает преждевременную сходимость), элитарные гонки (сохраняет лучшие конфигурации), параллельное выполнение. Превосходит стандартные конфигурации на ACOTSP, MOACO, SPEAR. Используется в оптимизации, ML, робототехнике. Открытый код.
- Ключевые слова: автоматическая конфигурация алгоритмов, итеративные гонки, I/F-Race, irace, настройка параметров, критерий Фридмана, R
- ГОСТ: López-Ibáñez M., Dubois-Lacoste J., Pérez Cáceres L., Birattari M., Stützle T. The irace package: Iterated racing for automatic algorithm configuration // Operations Research Perspectives. – 2016. – Vol. 3. – P. 43–58.

---

### ParamILS (AAAI 2007)
- Файл: [62__paramils-local-search-algorithm-configuration-2007.md](./paramils-local-search-algorithm-configuration-2007.md)
- Тема: Автоматическая конфигурация алгоритмов методом итеративного локального поиска (ParamILS) с поддержкой категориальных, числовых и условных параметров.
- Summary (EN): Introduces ParamILS for automatic algorithm configuration using iterated local search. BasicILS(N) uses fixed N training samples. FocusedILS adaptively increases samples for promising configurations, uses domination criterion, and bonus runs; provably converges to optimal configuration. Outperforms CALIBRA and defaults on SAT4J, SAPS, GLS⁺ (e.g., SAPS-SW: 6.0s vs 9.7s). Demonstrates over-tuning with small N. Handles conditional parameters. Open source. Speedups up to 10,000× on SAT instances.
- Сводка (RU): Представлен ParamILS для автоматической конфигурации алгоритмов методом итеративного локального поиска. BasicILS(N) использует фиксированные N запусков. FocusedILS адаптивно увеличивает число запусков для перспективных конфигураций, использует критерий доминирования и бонусные запуски; доказана сходимость к оптимальной конфигурации. Превосходит CALIBRA и стандартные настройки на SAT4J, SAPS, GLS⁺ (SAPS-SW: 6.0 с против 9.7 с). Продемонстрировано переобучение при малых N. Поддержка условных параметров. Открытый код. Ускорение до 10 000× на SAT-примерах.
- Ключевые слова: конфигурация алгоритмов, ParamILS, итеративный локальный поиск, настройка параметров, переобучение, SAT
- ГОСТ: Hutter F., Hoos H. H., Stützle T. Automatic Algorithm Configuration based on Local Search // Proceedings of the Twenty-Second AAAI Conference on Artificial Intelligence (AAAI-07). – 2007. – P. 1152–1157.

---

### Differential Evolution Survey (2011)
- Файл: [63__differential-evolution-state-of-the-art-survey-2011.md](./differential-evolution-state-of-the-art-survey-2011.md)
- Тема: Полный обзор метода дифференциальной эволюции (DE) — основные концепции, варианты, управление параметрами, теория, приложения.
- Summary (EN): Comprehensive survey of Differential Evolution (1995-2010). Covers classical DE/rand/1/bin, variants (TDE, ODE, DEGL, SaDE, JADE, jDE). Parameter adaptation (jDE, SaDE). Zaharie's critical F analysis. Rotation invariance only at Cr=1. Applications in power systems, electromagnetics, bioinformatics, signal processing. Drawbacks: poor on non-separable functions, weak selection pressure, no general convergence proof.
- Сводка (RU): Полный обзор метода дифференциальной эволюции (1995-2010). Охвачены классический DE/rand/1/bin, варианты (TDE, ODE, DEGL, SaDE, JADE, jDE). Адаптация параметров (jDE, SaDE). Анализ критического F Захари. Инвариантность к повороту только при Cr=1. Приложения в энергосистемах, электромагнетизме, биоинформатике, обработке сигналов. Недостатки: низкая эффективность на несепарабельных функциях, слабое селективное давление, отсутствие общего доказательства сходимости.
- Ключевые слова: дифференциальная эволюция, DE, эволюционные алгоритмы, глобальная оптимизация, самоадаптация, обзор
- ГОСТ: Das S., Suganthan P. N. Differential Evolution: A Survey of the State-of-the-Art // IEEE Transactions on Evolutionary Computation. – 2011. – Vol. 15, No. 1. – P. 4–31. DOI: 10.1109/TEVC.2010.2059031

---

### SMAC (LION 5, 2011) – Model-based Algorithm Configuration
- Файл: [64__smac-sequential-model-based-algorithm-configuration-2011.md](./smac-sequential-model-based-algorithm-configuration-2011.md)
- Тема: Два метода автоматической конфигурации алгоритмов: ROAR (случайный онлайн-агрессивный racing) и SMAC (последовательная конфигурация на основе случайного леса).
- Summary (EN): Presents ROAR (random online aggressive racing) and SMAC (sequential model-based algorithm configuration). SMAC uses random forest to predict runtime from configuration + instance features; selects promising configs; compares via aggressive racing. On 17 scenarios, SMAC improves over FocusedILS (0.93×–2.25×, 11/17 significant) and GGA (1.01×–2.76×, 13/17 significant). ROAR surprisingly effective baseline. Performance depends on instance features.
- Сводка (RU): Представлены ROAR (случайный онлайн-агрессивный racing) и SMAC (последовательная конфигурация на основе модели). SMAC использует случайный лес для предсказания времени работы по конфигурации + признакам экземпляра; выбирает перспективные конфигурации; сравнивает через агрессивный racing. На 17 сценариях SMAC улучшает FocusedILS (0.93×–2.25×, 11/17 значимо) и GGA (1.01×–2.76×, 13/17 значимо). ROAR неожиданно эффективен. Производительность зависит от признаков экземпляров.
- Ключевые слова: конфигурация алгоритмов, SMAC, случайный лес, model-based optimization, ROAR, racing, автоматическая настройка
- ГОСТ: Hutter F., Hoos H. H., Leyton-Brown K. Sequential Model-based Optimization for General Algorithm Configuration // Proceedings of Learning and Intelligent Optimization (LION 5). – 2011. – (слайды).

---

### SMAC-BBOB (GECCO 2013)
- Файл: [65__smac-bbob-evaluation-expensive-blackbox-2013.md](./smac-bbob-evaluation-expensive-blackbox-2013.md)
- Тема: Оценка SMAC-BBOB — варианта последовательной оптимизации на основе модели (GP) для дорогих непрерывных blackbox-функций на наборе BBOB.
- Summary (EN): Evaluates SMAC-BBOB (GP with Matérn kernel, EI acquisition) on BBOB benchmarks with small budgets. Outperforms CMA-ES on 13/24 functions for 10×D budget, especially separable/multimodal functions. Competitive with best BBOB-2009 results. For 100×D budget, CMA-ES catches up. O(N³) GP cost limits scalability. Recommended for very expensive functions with ≤10×D evaluations.
- Сводка (RU): Оценка SMAC-BBOB (GP с ядром Матерна, критерий EI) на наборе BBOB при малых бюджетах. Превосходит CMA-ES на 13/24 функциях при бюджете 10×D, особенно на сепарабельных и мультимодальных. Конкурентоспособен с лучшими результатами BBOB-2009. При бюджете 100×D CMA-ES догоняет. Сложность GP O(N³) ограничивает масштабируемость. Рекомендуется для очень дорогих функций с бюджетом ≤10×D вычислений.
- Ключевые слова: байесовская оптимизация, SMAC, BBOB, гауссовский процесс, ожидаемое улучшение, CMA-ES, дорогие функции, чёрный ящик
- ГОСТ: Hutter F., Hoos H. H., Leyton-Brown K. An Evaluation of Sequential Model-Based Optimization for Expensive Blackbox Functions // Proceedings of the 15th Annual Conference Companion on Genetic and Evolutionary Computation (GECCO '13 Companion). – New York: ACM, 2013. – P. 1209–1216. DOI: 10.1145/2464576.2501592

---

### Weighted Regression DFO (SIOPT 2013)
- Файл: [66__derivative-free-optimization-weighted-regression-2013.md](./derivative-free-optimization-weighted-regression-2013.md)
- Тема: Безградиентная оптимизация дорогих функций с вычислительной ошибкой с использованием взвешенной регрессии в CSV2-фреймворке.
- Summary (EN): Derivative-free trust-region optimization for expensive functions with computational error. Extends CSV2 framework with weighted least squares quadratic models. Generalizes Λ-poisedness to weighted regression. Weighting scheme balances Taylor error (∝ distance³) and computational error. On nondifferentiable and noisy benchmark problems, weighted regression outperforms interpolation and NEWUOA. O(n⁶) per iteration; not tested on stochastic noise.
- Сводка (RU): Безградиентная оптимизация в доверительной области для дорогих функций с вычислительной ошибкой. Обобщение CSV2-фреймворка с взвешенными квадратичными моделями. Расширение Λ-poisedness на взвешенную регрессию. Схема весов балансирует ошибку Тейлора (∝ расстояние³) и вычислительную ошибку. На недифференцируемых и зашумленных бенчмарках взвешенная регрессия превосходит интерполяцию и NEWUOA. Стоимость O(n⁶) на итерацию; не тестировался на стохастическом шуме.
- Ключевые слова: безградиентная оптимизация, доверительная область, взвешенная регрессия, дорогие функции, вычислительная ошибка, Λ-poisedness, CSV2, квадратичные модели
- ГОСТ: Custódio A. L., Scheinberg K., Vicente L. N. Derivative-Free Optimization of Expensive Functions with Computational Error Using Weighted Regression // SIAM Journal on Optimization. – 2013. – Vol. 23, No. 4. – P. 2096–2124.

---

### FFT extension for ECM/p±1 (Montgomery, 2017)
- Файл: [67__fft-extension-algebraic-group-factorization-2017.md](./fft-extension-algebraic-group-factorization-2017.md)
- Тема: FFT-расширение для второго этапа методов факторизации на эллиптических кривых (ECM) и p±1 с использованием быстрой полиномиальной арифметики.
- Summary (EN): Montgomery's FFT extension for stage two of ECM, p−1, p+1. Reduces complexity from Θ(B₂/log B₂) to Õ(√B₂) using product/remainder trees (POLYEVAL) or polynomial GCD (POLYGCD). Brent–Suyama extension uses higher powers; Dickson polynomials (deg 30) avoid clustering bias. Implemented in GMP-ECM. Example: 73-digit factor of 2¹¹⁶³−1 found with B₁=3·10⁹, B₂=10¹⁴.
- Сводка (RU): FFT-расширение Монтгомери для второго этапа ECM, p−1, p+1. Снижение сложности с Θ(B₂/log B₂) до Õ(√B₂) с использованием деревьев произведений/остатков (POLYEVAL) или НОД полиномов (POLYGCD). Расширение Брента–Суямы использует степени; полиномы Диксона (степени 30) избегают эффекта кластеризации. Реализовано в GMP-ECM. Пример: 73-значный фактор 2¹¹⁶³−1 найден с B₁=3·10⁹, B₂=10¹⁴.
- Ключевые слова: ECM, p−1, p+1, FFT, быстрое умножение полиномов, деревья произведений, полиномы Диксона, факторизация
- ГОСТ: Brent R. P., Kruppa A., Zimmermann P. FFT extension for algebraic-group factorization algorithms // Topics in Computational Number Theory Inspired by Peter L. Montgomery. – Cambridge University Press, 2017. – P. 189–205.

---

### Smooth Numbers in Factorization (Pomerance, ICM 1994)
- Файл: [68__smooth-numbers-in-factorization-and-discrete-logarithms-1994.md](./smooth-numbers-in-factorization-and-discrete-logarithms-1994.md)
- Тема: Обзор роли гладких чисел в современных алгоритмах факторизации, дискретного логарифма и проверки простоты.
- Summary (EN): Survey of smooth numbers (y-smooth: no prime factor >y) in computational number theory. Covers random squares (L(n)^{√2+o(1)}), quadratic sieve (L(n)^{1+o(1)}), number field sieve (L(n)^{1.526+o(1)}), elliptic curve method (L(p)^{1+o(1)}). Fundamental lemma: to find a square product among random integers up to x need ~L(x)^{√2} numbers. Index calculus for discrete logs (L(p)^{√2+o(1)}). Smooth p−1 used in APR-CL primality test and Carmichael number construction.
- Сводка (RU): Обзор роли гладких чисел (y-гладкие: нет простых делителей >y) в вычислительной теории чисел. Рассмотрены: случайные квадраты (L(n)^{√2+o(1)}), квадратичное решето (L(n)^{1+o(1)}), решето числового поля (L(n)^{1,526+o(1)}), метод эллиптических кривых (L(p)^{1+o(1)}). Фундаментальная лемма: для нахождения квадрата-произведения среди случайных чисел до x нужно ~L(x)^{√2} чисел. Индекс-исчисление для дискретных логарифмов (L(p)^{√2+o(1)}). Гладкость p−1 используется в тесте простоты APR-CL и построении чисел Кармайкла.
- Ключевые слова: гладкие числа, факторизация, квадратичное решето, решето числового поля, метод эллиптических кривых, дискретный логарифм, проверка простоты
- ГОСТ: Pomerance C. Smooth Numbers in Factorization and Discrete Logarithms // Proceedings of the International Congress of Mathematicians (ICM 1994), Zurich. – Birkhäuser, 1995. – Vol. 1. – P. 411–422.

---

### Differential Evolution (Storn, ICSI TR-95-012, 1995)
- Файл: [69__differential-evolution-original-technical-report-1995.md](./differential-evolution-original-technical-report-1995.md)
- Тема: Представление метода дифференциальной эволюции (DE) — первого публичного описания алгоритма, включая варианты DE1 и DE2, с экспериментальным сравнением против ASA и ANM.
- Summary (EN): First public description of Differential Evolution (DE1: v = x_r1 + F·(x_r2−x_r3); DE2: current-to-best). Tests on 10 functions (sphere, Rosenbrock, step, quartic, Shekel, Corana, Griewangk, Zimmermann, Chebyshev T₈/T₁₆). DE only method converging for all functions. Outperforms Adaptive Simulated Annealing (ASA) and Annealed Nelder-Mead (ANM), often by factor 2–10×. Parameter settings heuristic; no convergence proof.
- Сводка (RU): Первое публичное описание метода дифференциальной эволюции (DE1: v = x_r1 + F·(x_r2−x_r3); DE2: current-to-best). Тестирование на 10 функциях (сфера, Розенброк, ступенчатая, квартическая, Шекель, Корана, Гриванк, Циммерман, Чебышёв T₈/T₁₆). DE — единственный метод, сошедшийся для всех функций. Превосходит адаптивный имитационный отжиг (ASA) и анимированный Нелдер-Мид (ANM), часто в 2–10 раз. Выбор параметров эвристический; нет доказательства сходимости.
- Ключевые слова: дифференциальная эволюция, DE, глобальная оптимизация, эволюционные алгоритмы, имитационный отжиг, Нелдер-Мид, технический отчёт
- ГОСТ: Storn R. Differential Evolution - A Simple and Efficient Adaptive Scheme for Global Optimization over Continuous Spaces. – Berkeley: International Computer Science Institute, 1995. – Technical Report TR-95-012.

---



---



---



---



---