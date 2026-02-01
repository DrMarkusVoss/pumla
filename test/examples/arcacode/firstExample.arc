#PUMLAMR

# include the element definitions with alias E, F and G
# to use them in this definition
from ./../modelrepo_json.puml include E, F, G

# simple first example showing the language syntax

block display as "Display"
block sensorA as "TempSensor A"
block compute as "Compute Unit"

# signal chain
sensorA ---> compute ---> display


block x <<SystemA>>:
    internals:
        E
        F
    port A
    port B
    tag "System Variant"
    values ["A", "B1", "B2"]

block y as "huhu":
    port A
    port b as "B"
    port C:
        tag "vendor"
        values "SuperC Ltd."

block z:
    port C as "pCin"
    port D as "pDout"

    block z1 as "the Z1":
        port c1

    block z2:
        port c1
        port c2

    C ---> z1.c1
    C ---> z2.c1
    z2.c2 ---> D

    description:
        "this is a very important block. really"

    tag "important"

# different types of arrows

# dependency
x ...> y

# connection
x ---> y

# emphasized connection
x ===> y

# realization
x --r> y

# other way round also possible
y <r-- x

# composition
x --c> y

# named connection, can be referred to and modified (e.g. visibility) outside of definition)
# "myCon1" is the alias, the text in "" is the text shown on the arrow
x --->[myCon1 as "data flowing here"] y

# connections can also have stereotypes. if the alias is not specified, then it is an anonymous
# connection. it can not be referenced, but can have stereotypes or a name or both.
x ...>[myCon2 <<delegates>>] y

x.A ---> y.A
x.B ---> y.b

z.C ---> z.z1.c1
z.C ---> z.z2.c1

# connections must be specified outside of element definitions


####

# for software

# datastructure
struct X:
    int X
    float Y

# class

class Z:
    public:
        void callMe()
