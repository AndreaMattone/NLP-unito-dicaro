from concepts import Context
import graphviz
import os




c = Context.fromstring(
    '''
                |coccodrillo|gallina|cane|cinghiale |
 pericoloso     |  x        |       |    |     x    |
 addomesticato  |           |       |  x |          |
 edibile        |           |  x    |    |     x    |
 mammifero      |           |       |  x |     x    |
 '''
)

for extent, intent in c.lattice:
    print('%r %r' % (extent, intent))

c.lattice.graphviz(view=True)
