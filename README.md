# Compilers

В данном проекте реализован компилятор в JVM bytecode примитивного языка, поддерживающего переменные, арифметические выражения, функции, потоки и другие особенности.
Можно называть этот язык "dc" или "dark chars", потому что написание программ на нем, скорее всего, доставит много боли, как и одна японская игра с аналогичным префиксом в названии.

## Поддерживаемые типы

Данный язык поддерживает типы bool, int, long, float, double, str. Строки в данном языке неизменяемы.
Константы выглядят следующим образом:
* bool: `true`, `false`
* int: `1`, `-5`, `0`
* long: `1l`, `1000000000000l` -- длинные числа имеют суффикс "l"
* float: `1.001`, `-23.0` -- числа с плавающей точкой обязаны иметь хотя бы одну цифру до и после точки
* double: `2.718281828459045d` -- все так же, как у float, толкьо есть суффикс "d" 
* str: "it's sample string" -- используются двойные кавычки, одинарные могут находиться внутри строки

## Структура программы

Программа на языке dc состоит из последовательности команд, функций и потоков.

### Команды

* Variable declaration: variable_type variable name [= initial_expression]; -- объявление новой переменой. Примеры: 
 * `int a;`
 * `str s = "Hello";`
* Union declaration: union union_name { union_fields }; -- объявление нового union (несколько переменных разных типов, хранящихся в одном месте памяти. Пример:
```c++
    union u {
        int int_value;
        double double_value;
    }
```
* Assignment: variable = expression; -- присвоение переменной значения. Переменная может быть полем union. Примеры:
 * `a = 1;`
 * `u.double_value = 1.0d;`
 * `u.double_value = 1.0;`
 * Чуть позже я прокомментирую отичие между двумя примерами выше
 
* Loop: while expression { commands } -- цикл while в классическом смысле
```
while (true) {
    write "I'll always will pass my exams in time";
}
```
* Condition: if expression { commands } [else { commands }] -- самый обычный if
```
if true {
    write "it will be said";
} else {
    write "it will stay secret";
}
```
* Read: read variable_name; -- чтение переменной из stdin
```
read a;
```
* Write: write expression; -- вывод значения выражения в stdout
```
write a + a;
```
* Return: return [expression]; -- вернуть занчение выражения или просто выйти из функции, если выражения нет:
 * `return;`
 * `return 0;`
* Function call: function_name (arguments); -- вызвать функцию. Аргументы -- множество выражений, перечисленных через запятую (возможно, пустое):
 * `foo();`
 * `goo(1);`
* Tread call: thread_name (); -- запустить поток. Подробнее в разделе "Потоки".
* Lock: [un]lock variable_name; -- взять [отпустить] блокировку по переменной. Можно делать только со строками, потому что они единственные объекты, а остальные типы являются примитивными.
```
lock s;
# perform some actions in critical section
unlock s;
```
* Block: { commands } -- блок комманд со своими локальными переменными


### Выражения

Рассмотрим операции по их приоритету (от самого низкого к наивысшему)

* `||`, `V` -- "или" и "стрелка Пирса"
* `&&`, `|` -- "и" и "штрих Шеффера"
* `==`, `>=`, `>`, `<=`, `<=`, `!=` -- операции сравнения
* `+`, `-` -- операции сложения и вычитания
* `*`, `/`, `%` -- умножение, деление и остаток от деления
* `(type)` -- cast выражения к указанному типу: `(int) 2.0`
* `=` -- присвоение. В левой части может стоять только имя переменной

Терминалами в дереве разбора выражений могут быть константы, переменные или вызовы функций.
Также когда два операнда какой-либо операции имеют разный тип, то результат опреации будет иметь их наименьший общий надтип.
Строки не могут приведены ни к одному типу и наоборот.
Иерархия типов задается двумя цепочками:
`bool -> int -> long -> double`
`float -> double`

Чуть позже планируется добавить оптимизацию вычисления логических выражений, когда если мы имеем несколько "или" подряд, то получив истинность одного из них, мы можем не вычислять оставшиеся и перейти к выражению после ближайшей стрелки Пирса или, если такой нет, то к концу выражения. Аналогичная оптимизация планируется и для "и".

### Функции

Функции можно объявить без определения: `int f(str arg);`. После объявления данную функцию можно вызывать.
Определение функции выглядит похожим образом:
```
int g(str arg1, int arg2)
{
  #some commands here
}
```

### Потоки

Поток является отдельной программой, которая видит поля главного класса и может читать и записывать их значения, а также брать блокировки по ним (только по строкам).
То есть каждый поток имеет свои методы и свои глобальные переменные, видимые из всех его методов.
Ни переменные, ни методы не видны из вне потока.
Можно запускать несколько потоков одного типа параллельно.


## Запуск программы на языке dc

Для того, чтобы запустить код на данном языке, вам понадобятся:
* Два питона: Python2.7 и Python3.5
* На Python3.5 требуется установить runtime antlr4 с помощью команды `pip3 install antlr4-python3-runtime`
* JVM для запуска скомпилированных .class файлов

Автор понимает, что использование двух разных питонов в одном проекте выглядит не слишком красивым. Однако он до последнего пытался найти другой ассамблер в JVM для третьего питона, однако эти попытки не увенчались успехом.
Желательно, чтобы у Вас был установлен только один третий питон и только один второй, чтобы быть уверенным, что будет вызван нужный pip.

Итак, usage:
* Компиляция происходит с помощью запуска скрипта `./compile.sh [-p] sourse_code.dc`. Параметр `-p` также выведет дерево разбора файла. При этом файлы .class помещаются в директорию `out/`. В этой директории будут также находиться файлы с промежуточным кодом .j, чуть позже будет добавлен флаг для их удаления после компиляции.
* Запуск скомпилированных .class файлов происходит с помощью команды `java -cp out/ classname`, где `classname` -- название файла с исходным кодом без расширения.

Для пользователей Windows все аналогично, кроме того, что запускать надо скрипт `./compile.cmd`

## Оптимизации

В данном языке реализованы две оптимизации:
* Оптимизация вычисления логических выражений
* Удаление необязательных присвоений

Первая оптимизации заключается в том, что если мы применяем операцию &&  к нескольким выражениям подряд и одно из них было вычислено как ложь, то остальные можно не вычислять.
Данную оптимизацию чуть усложняет наличие штриха Шеффера в языке, имеющий тот же приоритет, что и &&.
Сложность в том, что если все выражение перед штрихом -- ложь, то после него оно станет истинным.
Поэтому мы не можем однозначно сказать значение всего логического выражения, не зная значения логических выражений через одно после штриха Шеффера, и их приходится вычислять (однако если одно из них оказалось ложью, то мы можем снова перепрыгнуть либо за ближайший штрих, либо в конец всего выражения).
Аналогичная оптимизация есть и для || со стрелкой Пирса.

Вторая оптимизация в момент присвоения значений локальным переменным или при выходе из зоны их видимости проверяет, были ли эти переменные задействованы со времени своего последнего присвоения.
Если нет, то компилятор находит последнее присвоение и аккуратно удаляет его.
Это вызывает некоторые сложности. Например, в цикле while теперь нельзя использовать выражения-присвоения, если после while переменная не будет использована:
```
while a = a + 1 {
    # No usage of "a" in the loop
    ...
}
# No more usage of "a" here
```
Это происходит потому, что с точки зрения компилятора в выражении для while происходит последнее присвоение для переменной a.
В дальнейшем, наверное, это будет исправлено.
Хотя случаи `a = (b = a + 1)` будет все также сложно учесть, если не считать все присвоения в выражении для while нужными.
Но пока лучше не рисковать и не использовать присвоения в выражении для while.