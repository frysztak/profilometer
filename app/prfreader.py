import parse
import numpy as np


class PRFreader:
    @classmethod
    def read(self, filename):
        self.header_tmpl = """1 2
{} 0.000000e+000 PRF
CX M {cntX:e} MM 1.000000e+000 D
CZ M {cntZ:e} MM {scale:e} L
EOR
STYLUS_RADIUS 0.000000e+000 MM
SPACING CX {spacingX:e}
MAP 1.000000e+000 CZ CZ 1.000000e+000 1.000000e+000
MAP 2.000000e+000 CZ CX 1.000000e+000 0.000000e+000
EOR
"""
        with open(filename) as f:
            header = ''.join([next(f) for x in range(10)])
            params = parse.search(self.header_tmpl, header)

            cnt = int(params['cntX'])
            scale = params['scale']
            spacing = params['spacingX']

            data = [float(next(f).strip()) for x in range(cnt)]
        data = scale * np.array(data, dtype=np.float)
        return (spacing, data)
