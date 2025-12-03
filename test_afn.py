import unittest
from afn import Estado, AFN
from conversor import ConversorERparaAFN
from reconhecedor import ReconhecedorAFN


class TestEstado(unittest.TestCase):
    def setUp(self):
        Estado.contador = 0
    
    def test_criacao_estado(self):
        e = Estado()
        self.assertEqual(e.id, 0)
        self.assertFalse(e.eh_final)
        self.assertEqual(len(e.transicoes), 0)
    
    def test_adicionar_transicao(self):
        e1 = Estado()
        e2 = Estado()
        e1.adicionar_transicao('a', e2)
        self.assertIn('a', e1.transicoes)
        self.assertEqual(e1.transicoes['a'], [e2])
    
    def test_multiplas_transicoes_mesmo_simbolo(self):
        e1 = Estado()
        e2 = Estado()
        e3 = Estado()
        e1.adicionar_transicao('a', e2)
        e1.adicionar_transicao('a', e3)
        self.assertEqual(len(e1.transicoes['a']), 2)


class TestAFN(unittest.TestCase):
    def setUp(self):
        Estado.contador = 0
    
    def test_criacao_afn_simples(self):
        inicial = Estado()
        final = Estado()
        afn = AFN(inicial, final)
        self.assertEqual(afn.estado_inicial, inicial)
        self.assertEqual(afn.estado_final, final)
        self.assertTrue(final.eh_final)
    
    def test_obter_todos_estados(self):
        inicial = Estado()
        intermediario = Estado()
        final = Estado()
        inicial.adicionar_transicao('a', intermediario)
        intermediario.adicionar_transicao('b', final)
        afn = AFN(inicial, final)
        estados = afn.obter_todos_estados()
        self.assertEqual(len(estados), 3)


class TestConversorSimboloSimples(unittest.TestCase):
    def setUp(self):
        Estado.contador = 0
    
    def test_converter_a(self):
        conversor = ConversorERparaAFN('a')
        afn = conversor.converter()
        self.assertIsNotNone(afn)
        estados = afn.obter_todos_estados()
        self.assertEqual(len(estados), 2)
    
    def test_converter_b(self):
        conversor = ConversorERparaAFN('b')
        afn = conversor.converter()
        estados = afn.obter_todos_estados()
        self.assertEqual(len(estados), 2)
    
    def test_converter_0(self):
        conversor = ConversorERparaAFN('0')
        afn = conversor.converter()
        estados = afn.obter_todos_estados()
        self.assertEqual(len(estados), 2)


class TestConversorConcatenacao(unittest.TestCase):
    def setUp(self):
        Estado.contador = 0
    
    def test_converter_ab(self):
        conversor = ConversorERparaAFN('ab')
        afn = conversor.converter()
        estados = afn.obter_todos_estados()
        self.assertGreater(len(estados), 2)
    
    def test_converter_abc(self):
        conversor = ConversorERparaAFN('abc')
        afn = conversor.converter()
        estados = afn.obter_todos_estados()
        self.assertGreater(len(estados), 3)


class TestConversorUniao(unittest.TestCase):
    def setUp(self):
        Estado.contador = 0
    
    def test_converter_a_ou_b(self):
        conversor = ConversorERparaAFN('a|b')
        afn = conversor.converter()
        estados = afn.obter_todos_estados()
        self.assertGreater(len(estados), 2)
    
    def test_converter_a_ou_b_ou_c(self):
        conversor = ConversorERparaAFN('a|b|c')
        afn = conversor.converter()
        estados = afn.obter_todos_estados()
        self.assertGreater(len(estados), 4)


class TestConversorKleene(unittest.TestCase):
    def setUp(self):
        Estado.contador = 0
    
    def test_converter_a_estrela(self):
        conversor = ConversorERparaAFN('a*')
        afn = conversor.converter()
        estados = afn.obter_todos_estados()
        self.assertGreater(len(estados), 2)
    
    def test_converter_ab_estrela(self):
        conversor = ConversorERparaAFN('(ab)*')
        afn = conversor.converter()
        estados = afn.obter_todos_estados()
        self.assertGreater(len(estados), 4)


class TestReconhecimentoSimples(unittest.TestCase):
    def setUp(self):
        Estado.contador = 0
    
    def test_reconhecer_a_aceita_a(self):
        conversor = ConversorERparaAFN('a')
        afn = conversor.converter()
        reconhecedor = ReconhecedorAFN(afn)
        aceita, _ = reconhecedor.reconhecer('a')
        self.assertTrue(aceita)
    
    def test_reconhecer_a_rejeita_b(self):
        conversor = ConversorERparaAFN('a')
        afn = conversor.converter()
        reconhecedor = ReconhecedorAFN(afn)
        aceita, _ = reconhecedor.reconhecer('b')
        self.assertFalse(aceita)
    
    def test_reconhecer_ab_aceita_ab(self):
        conversor = ConversorERparaAFN('ab')
        afn = conversor.converter()
        reconhecedor = ReconhecedorAFN(afn)
        aceita, _ = reconhecedor.reconhecer('ab')
        self.assertTrue(aceita)
    
    def test_reconhecer_ab_rejeita_a(self):
        conversor = ConversorERparaAFN('ab')
        afn = conversor.converter()
        reconhecedor = ReconhecedorAFN(afn)
        aceita, _ = reconhecedor.reconhecer('a')
        self.assertFalse(aceita)


class TestReconhecimentoUniao(unittest.TestCase):
    def setUp(self):
        Estado.contador = 0
    
    def test_a_ou_b_aceita_a(self):
        conversor = ConversorERparaAFN('a|b')
        afn = conversor.converter()
        reconhecedor = ReconhecedorAFN(afn)
        aceita, _ = reconhecedor.reconhecer('a')
        self.assertTrue(aceita)
    
    def test_a_ou_b_aceita_b(self):
        conversor = ConversorERparaAFN('a|b')
        afn = conversor.converter()
        reconhecedor = ReconhecedorAFN(afn)
        aceita, _ = reconhecedor.reconhecer('b')
        self.assertTrue(aceita)
    
    def test_a_ou_b_rejeita_c(self):
        conversor = ConversorERparaAFN('a|b')
        afn = conversor.converter()
        reconhecedor = ReconhecedorAFN(afn)
        aceita, _ = reconhecedor.reconhecer('c')
        self.assertFalse(aceita)


class TestReconhecimentoKleene(unittest.TestCase):
    def setUp(self):
        Estado.contador = 0
    
    def test_a_estrela_aceita_vazio(self):
        conversor = ConversorERparaAFN('a*')
        afn = conversor.converter()
        reconhecedor = ReconhecedorAFN(afn)
        aceita, _ = reconhecedor.reconhecer('')
        self.assertTrue(aceita)
    
    def test_a_estrela_aceita_a(self):
        conversor = ConversorERparaAFN('a*')
        afn = conversor.converter()
        reconhecedor = ReconhecedorAFN(afn)
        aceita, _ = reconhecedor.reconhecer('a')
        self.assertTrue(aceita)
    
    def test_a_estrela_aceita_aa(self):
        conversor = ConversorERparaAFN('a*')
        afn = conversor.converter()
        reconhecedor = ReconhecedorAFN(afn)
        aceita, _ = reconhecedor.reconhecer('aa')
        self.assertTrue(aceita)
    
    def test_a_estrela_aceita_aaa(self):
        conversor = ConversorERparaAFN('a*')
        afn = conversor.converter()
        reconhecedor = ReconhecedorAFN(afn)
        aceita, _ = reconhecedor.reconhecer('aaa')
        self.assertTrue(aceita)
    
    def test_a_estrela_rejeita_b(self):
        conversor = ConversorERparaAFN('a*')
        afn = conversor.converter()
        reconhecedor = ReconhecedorAFN(afn)
        aceita, _ = reconhecedor.reconhecer('b')
        self.assertFalse(aceita)


class TestReconhecimentoComplexo(unittest.TestCase):
    def setUp(self):
        Estado.contador = 0
    
    def test_ab_ou_cd_aceita_ab(self):
        conversor = ConversorERparaAFN('ab|cd')
        afn = conversor.converter()
        reconhecedor = ReconhecedorAFN(afn)
        aceita, _ = reconhecedor.reconhecer('ab')
        self.assertTrue(aceita)
    
    def test_ab_ou_cd_aceita_cd(self):
        conversor = ConversorERparaAFN('ab|cd')
        afn = conversor.converter()
        reconhecedor = ReconhecedorAFN(afn)
        aceita, _ = reconhecedor.reconhecer('cd')
        self.assertTrue(aceita)
    
    def test_ab_ou_cd_rejeita_ac(self):
        conversor = ConversorERparaAFN('ab|cd')
        afn = conversor.converter()
        reconhecedor = ReconhecedorAFN(afn)
        aceita, _ = reconhecedor.reconhecer('ac')
        self.assertFalse(aceita)
    
    def test_a_ou_b_estrela_aceita_vazio(self):
        conversor = ConversorERparaAFN('(a|b)*')
        afn = conversor.converter()
        reconhecedor = ReconhecedorAFN(afn)
        aceita, _ = reconhecedor.reconhecer('')
        self.assertTrue(aceita)
    
    def test_a_ou_b_estrela_aceita_a(self):
        conversor = ConversorERparaAFN('(a|b)*')
        afn = conversor.converter()
        reconhecedor = ReconhecedorAFN(afn)
        aceita, _ = reconhecedor.reconhecer('a')
        self.assertTrue(aceita)
    
    def test_a_ou_b_estrela_aceita_ab(self):
        conversor = ConversorERparaAFN('(a|b)*')
        afn = conversor.converter()
        reconhecedor = ReconhecedorAFN(afn)
        aceita, _ = reconhecedor.reconhecer('ab')
        self.assertTrue(aceita)
    
    def test_a_ou_b_estrela_aceita_abba(self):
        conversor = ConversorERparaAFN('(a|b)*')
        afn = conversor.converter()
        reconhecedor = ReconhecedorAFN(afn)
        aceita, _ = reconhecedor.reconhecer('abba')
        self.assertTrue(aceita)
    
    def test_a_ou_b_estrela_rejeita_c(self):
        conversor = ConversorERparaAFN('(a|b)*')
        afn = conversor.converter()
        reconhecedor = ReconhecedorAFN(afn)
        aceita, _ = reconhecedor.reconhecer('c')
        self.assertFalse(aceita)


class TestReconhecimentoNumeros(unittest.TestCase):
    def setUp(self):
        Estado.contador = 0
    
    def test_0_ou_1_aceita_0(self):
        conversor = ConversorERparaAFN('0|1')
        afn = conversor.converter()
        reconhecedor = ReconhecedorAFN(afn)
        aceita, _ = reconhecedor.reconhecer('0')
        self.assertTrue(aceita)
    
    def test_0_ou_1_aceita_1(self):
        conversor = ConversorERparaAFN('0|1')
        afn = conversor.converter()
        reconhecedor = ReconhecedorAFN(afn)
        aceita, _ = reconhecedor.reconhecer('1')
        self.assertTrue(aceita)
    
    def test_0_ou_1_estrela_aceita_01(self):
        conversor = ConversorERparaAFN('(0|1)*')
        afn = conversor.converter()
        reconhecedor = ReconhecedorAFN(afn)
        aceita, _ = reconhecedor.reconhecer('01')
        self.assertTrue(aceita)
    
    def test_0_ou_1_estrela_aceita_1010(self):
        conversor = ConversorERparaAFN('(0|1)*')
        afn = conversor.converter()
        reconhecedor = ReconhecedorAFN(afn)
        aceita, _ = reconhecedor.reconhecer('1010')
        self.assertTrue(aceita)


class TestReconhecimentoCadeiaVazia(unittest.TestCase):
    def setUp(self):
        Estado.contador = 0
    
    def test_a_rejeita_vazio(self):
        conversor = ConversorERparaAFN('a')
        afn = conversor.converter()
        reconhecedor = ReconhecedorAFN(afn)
        aceita, _ = reconhecedor.reconhecer('')
        self.assertFalse(aceita)
    
    def test_ab_rejeita_vazio(self):
        conversor = ConversorERparaAFN('ab')
        afn = conversor.converter()
        reconhecedor = ReconhecedorAFN(afn)
        aceita, _ = reconhecedor.reconhecer('')
        self.assertFalse(aceita)


class TestReconhecimentoParenteses(unittest.TestCase):
    def setUp(self):
        Estado.contador = 0
    
    def test_a_b_concatenacao_aceita_ab(self):
        conversor = ConversorERparaAFN('(a)(b)')
        afn = conversor.converter()
        reconhecedor = ReconhecedorAFN(afn)
        aceita, _ = reconhecedor.reconhecer('ab')
        self.assertTrue(aceita)
    
    def test_a_ou_b_c_aceita_ac(self):
        conversor = ConversorERparaAFN('(a|b)c')
        afn = conversor.converter()
        reconhecedor = ReconhecedorAFN(afn)
        aceita, _ = reconhecedor.reconhecer('ac')
        self.assertTrue(aceita)
    
    def test_a_ou_b_c_aceita_bc(self):
        conversor = ConversorERparaAFN('(a|b)c')
        afn = conversor.converter()
        reconhecedor = ReconhecedorAFN(afn)
        aceita, _ = reconhecedor.reconhecer('bc')
        self.assertTrue(aceita)
    
    def test_a_b_ou_c_aceita_ab(self):
        conversor = ConversorERparaAFN('a(b|c)')
        afn = conversor.converter()
        reconhecedor = ReconhecedorAFN(afn)
        aceita, _ = reconhecedor.reconhecer('ab')
        self.assertTrue(aceita)
    
    def test_a_b_ou_c_aceita_ac(self):
        conversor = ConversorERparaAFN('a(b|c)')
        afn = conversor.converter()
        reconhecedor = ReconhecedorAFN(afn)
        aceita, _ = reconhecedor.reconhecer('ac')
        self.assertTrue(aceita)


class TestReconhecimentoAvancado(unittest.TestCase):
    def setUp(self):
        Estado.contador = 0
    
    def test_aa_estrela_aceita_vazio(self):
        conversor = ConversorERparaAFN('(aa)*')
        afn = conversor.converter()
        reconhecedor = ReconhecedorAFN(afn)
        aceita, _ = reconhecedor.reconhecer('')
        self.assertTrue(aceita)
    
    def test_aa_estrela_aceita_aa(self):
        conversor = ConversorERparaAFN('(aa)*')
        afn = conversor.converter()
        reconhecedor = ReconhecedorAFN(afn)
        aceita, _ = reconhecedor.reconhecer('aa')
        self.assertTrue(aceita)
    
    def test_aa_estrela_aceita_aaaa(self):
        conversor = ConversorERparaAFN('(aa)*')
        afn = conversor.converter()
        reconhecedor = ReconhecedorAFN(afn)
        aceita, _ = reconhecedor.reconhecer('aaaa')
        self.assertTrue(aceita)
    
    def test_aa_estrela_rejeita_a(self):
        conversor = ConversorERparaAFN('(aa)*')
        afn = conversor.converter()
        reconhecedor = ReconhecedorAFN(afn)
        aceita, _ = reconhecedor.reconhecer('a')
        self.assertFalse(aceita)
    
    def test_aa_estrela_rejeita_aaa(self):
        conversor = ConversorERparaAFN('(aa)*')
        afn = conversor.converter()
        reconhecedor = ReconhecedorAFN(afn)
        aceita, _ = reconhecedor.reconhecer('aaa')
        self.assertFalse(aceita)


class TestConversorCaracteresEspeciais(unittest.TestCase):
    def setUp(self):
        Estado.contador = 0
    
    def test_converter_x(self):
        conversor = ConversorERparaAFN('x')
        afn = conversor.converter()
        estados = afn.obter_todos_estados()
        self.assertEqual(len(estados), 2)
    
    def test_converter_y(self):
        conversor = ConversorERparaAFN('y')
        afn = conversor.converter()
        estados = afn.obter_todos_estados()
        self.assertEqual(len(estados), 2)
    
    def test_converter_z(self):
        conversor = ConversorERparaAFN('z')
        afn = conversor.converter()
        estados = afn.obter_todos_estados()
        self.assertEqual(len(estados), 2)


class TestReconhecimentoConcatenacaoLonga(unittest.TestCase):
    def setUp(self):
        Estado.contador = 0
    
    def test_abcd_aceita_abcd(self):
        conversor = ConversorERparaAFN('abcd')
        afn = conversor.converter()
        reconhecedor = ReconhecedorAFN(afn)
        aceita, _ = reconhecedor.reconhecer('abcd')
        self.assertTrue(aceita)
    
    def test_abcd_rejeita_abc(self):
        conversor = ConversorERparaAFN('abcd')
        afn = conversor.converter()
        reconhecedor = ReconhecedorAFN(afn)
        aceita, _ = reconhecedor.reconhecer('abc')
        self.assertFalse(aceita)
    
    def test_abcde_aceita_abcde(self):
        conversor = ConversorERparaAFN('abcde')
        afn = conversor.converter()
        reconhecedor = ReconhecedorAFN(afn)
        aceita, _ = reconhecedor.reconhecer('abcde')
        self.assertTrue(aceita)


class TestReconhecimentoUniaoMultipla(unittest.TestCase):
    def setUp(self):
        Estado.contador = 0
    
    def test_a_ou_b_ou_c_ou_d_aceita_a(self):
        conversor = ConversorERparaAFN('a|b|c|d')
        afn = conversor.converter()
        reconhecedor = ReconhecedorAFN(afn)
        aceita, _ = reconhecedor.reconhecer('a')
        self.assertTrue(aceita)
    
    def test_a_ou_b_ou_c_ou_d_aceita_d(self):
        conversor = ConversorERparaAFN('a|b|c|d')
        afn = conversor.converter()
        reconhecedor = ReconhecedorAFN(afn)
        aceita, _ = reconhecedor.reconhecer('d')
        self.assertTrue(aceita)
    
    def test_a_ou_b_ou_c_ou_d_rejeita_e(self):
        conversor = ConversorERparaAFN('a|b|c|d')
        afn = conversor.converter()
        reconhecedor = ReconhecedorAFN(afn)
        aceita, _ = reconhecedor.reconhecer('e')
        self.assertFalse(aceita)


class TestReconhecimentoKleeneMultiplo(unittest.TestCase):
    def setUp(self):
        Estado.contador = 0
    
    def test_b_estrela_aceita_vazio(self):
        conversor = ConversorERparaAFN('b*')
        afn = conversor.converter()
        reconhecedor = ReconhecedorAFN(afn)
        aceita, _ = reconhecedor.reconhecer('')
        self.assertTrue(aceita)
    
    def test_b_estrela_aceita_bbb(self):
        conversor = ConversorERparaAFN('b*')
        afn = conversor.converter()
        reconhecedor = ReconhecedorAFN(afn)
        aceita, _ = reconhecedor.reconhecer('bbb')
        self.assertTrue(aceita)
    
    def test_abc_estrela_aceita_vazio(self):
        conversor = ConversorERparaAFN('(abc)*')
        afn = conversor.converter()
        reconhecedor = ReconhecedorAFN(afn)
        aceita, _ = reconhecedor.reconhecer('')
        self.assertTrue(aceita)
    
    def test_abc_estrela_aceita_abc(self):
        conversor = ConversorERparaAFN('(abc)*')
        afn = conversor.converter()
        reconhecedor = ReconhecedorAFN(afn)
        aceita, _ = reconhecedor.reconhecer('abc')
        self.assertTrue(aceita)
    
    def test_abc_estrela_aceita_abcabc(self):
        conversor = ConversorERparaAFN('(abc)*')
        afn = conversor.converter()
        reconhecedor = ReconhecedorAFN(afn)
        aceita, _ = reconhecedor.reconhecer('abcabc')
        self.assertTrue(aceita)
    
    def test_abc_estrela_rejeita_ab(self):
        conversor = ConversorERparaAFN('(abc)*')
        afn = conversor.converter()
        reconhecedor = ReconhecedorAFN(afn)
        aceita, _ = reconhecedor.reconhecer('ab')
        self.assertFalse(aceita)


class TestReconhecimentoMisto(unittest.TestCase):
    def setUp(self):
        Estado.contador = 0
    
    def test_a_estrela_b_aceita_b(self):
        conversor = ConversorERparaAFN('a*b')
        afn = conversor.converter()
        reconhecedor = ReconhecedorAFN(afn)
        aceita, _ = reconhecedor.reconhecer('b')
        self.assertTrue(aceita)
    
    def test_a_estrela_b_aceita_ab(self):
        conversor = ConversorERparaAFN('a*b')
        afn = conversor.converter()
        reconhecedor = ReconhecedorAFN(afn)
        aceita, _ = reconhecedor.reconhecer('ab')
        self.assertTrue(aceita)
    
    def test_a_estrela_b_aceita_aaab(self):
        conversor = ConversorERparaAFN('a*b')
        afn = conversor.converter()
        reconhecedor = ReconhecedorAFN(afn)
        aceita, _ = reconhecedor.reconhecer('aaab')
        self.assertTrue(aceita)
    
    def test_a_estrela_b_rejeita_a(self):
        conversor = ConversorERparaAFN('a*b')
        afn = conversor.converter()
        reconhecedor = ReconhecedorAFN(afn)
        aceita, _ = reconhecedor.reconhecer('a')
        self.assertFalse(aceita)
    
    def test_a_b_estrela_aceita_a(self):
        conversor = ConversorERparaAFN('ab*')
        afn = conversor.converter()
        reconhecedor = ReconhecedorAFN(afn)
        aceita, _ = reconhecedor.reconhecer('a')
        self.assertTrue(aceita)
    
    def test_a_b_estrela_aceita_abbb(self):
        conversor = ConversorERparaAFN('ab*')
        afn = conversor.converter()
        reconhecedor = ReconhecedorAFN(afn)
        aceita, _ = reconhecedor.reconhecer('abbb')
        self.assertTrue(aceita)


class TestReconhecimentoParentesesAninhados(unittest.TestCase):
    def setUp(self):
        Estado.contador = 0
    
    def test_a_ou_bc_aceita_a(self):
        conversor = ConversorERparaAFN('a|(bc)')
        afn = conversor.converter()
        reconhecedor = ReconhecedorAFN(afn)
        aceita, _ = reconhecedor.reconhecer('a')
        self.assertTrue(aceita)
    
    def test_a_ou_bc_aceita_bc(self):
        conversor = ConversorERparaAFN('a|(bc)')
        afn = conversor.converter()
        reconhecedor = ReconhecedorAFN(afn)
        aceita, _ = reconhecedor.reconhecer('bc')
        self.assertTrue(aceita)
    
    def test_ab_ou_c_estrela_aceita_ab(self):
        conversor = ConversorERparaAFN('(ab|c)*')
        afn = conversor.converter()
        reconhecedor = ReconhecedorAFN(afn)
        aceita, _ = reconhecedor.reconhecer('ab')
        self.assertTrue(aceita)
    
    def test_ab_ou_c_estrela_aceita_c(self):
        conversor = ConversorERparaAFN('(ab|c)*')
        afn = conversor.converter()
        reconhecedor = ReconhecedorAFN(afn)
        aceita, _ = reconhecedor.reconhecer('c')
        self.assertTrue(aceita)
    
    def test_ab_ou_c_estrela_aceita_abcab(self):
        conversor = ConversorERparaAFN('(ab|c)*')
        afn = conversor.converter()
        reconhecedor = ReconhecedorAFN(afn)
        aceita, _ = reconhecedor.reconhecer('abcab')
        self.assertTrue(aceita)


class TestReconhecimentoSequencial(unittest.TestCase):
    def setUp(self):
        Estado.contador = 0
    
    def test_xyz_aceita_xyz(self):
        conversor = ConversorERparaAFN('xyz')
        afn = conversor.converter()
        reconhecedor = ReconhecedorAFN(afn)
        aceita, _ = reconhecedor.reconhecer('xyz')
        self.assertTrue(aceita)
    
    def test_xyz_rejeita_xy(self):
        conversor = ConversorERparaAFN('xyz')
        afn = conversor.converter()
        reconhecedor = ReconhecedorAFN(afn)
        aceita, _ = reconhecedor.reconhecer('xy')
        self.assertFalse(aceita)
    
    def test_123_aceita_123(self):
        conversor = ConversorERparaAFN('123')
        afn = conversor.converter()
        reconhecedor = ReconhecedorAFN(afn)
        aceita, _ = reconhecedor.reconhecer('123')
        self.assertTrue(aceita)


class TestReconhecimentoComplexoMisto(unittest.TestCase):
    def setUp(self):
        Estado.contador = 0
    
    def test_a_estrela_b_ou_c_aceita_b(self):
        conversor = ConversorERparaAFN('a*(b|c)')
        afn = conversor.converter()
        reconhecedor = ReconhecedorAFN(afn)
        aceita, _ = reconhecedor.reconhecer('b')
        self.assertTrue(aceita)
    
    def test_a_estrela_b_ou_c_aceita_c(self):
        conversor = ConversorERparaAFN('a*(b|c)')
        afn = conversor.converter()
        reconhecedor = ReconhecedorAFN(afn)
        aceita, _ = reconhecedor.reconhecer('c')
        self.assertTrue(aceita)
    
    def test_a_estrela_b_ou_c_aceita_aaab(self):
        conversor = ConversorERparaAFN('a*(b|c)')
        afn = conversor.converter()
        reconhecedor = ReconhecedorAFN(afn)
        aceita, _ = reconhecedor.reconhecer('aaab')
        self.assertTrue(aceita)
    
    def test_a_estrela_b_ou_c_aceita_aaac(self):
        conversor = ConversorERparaAFN('a*(b|c)')
        afn = conversor.converter()
        reconhecedor = ReconhecedorAFN(afn)
        aceita, _ = reconhecedor.reconhecer('aaac')
        self.assertTrue(aceita)
    
    def test_a_ou_b_c_estrela_aceita_ac(self):
        conversor = ConversorERparaAFN('(a|b)c*')
        afn = conversor.converter()
        reconhecedor = ReconhecedorAFN(afn)
        aceita, _ = reconhecedor.reconhecer('ac')
        self.assertTrue(aceita)
    
    def test_a_ou_b_c_estrela_aceita_bccc(self):
        conversor = ConversorERparaAFN('(a|b)c*')
        afn = conversor.converter()
        reconhecedor = ReconhecedorAFN(afn)
        aceita, _ = reconhecedor.reconhecer('bccc')
        self.assertTrue(aceita)


class TestReconhecimentoBinario(unittest.TestCase):
    def setUp(self):
        Estado.contador = 0
    
    def test_0_estrela_1_aceita_1(self):
        conversor = ConversorERparaAFN('0*1')
        afn = conversor.converter()
        reconhecedor = ReconhecedorAFN(afn)
        aceita, _ = reconhecedor.reconhecer('1')
        self.assertTrue(aceita)
    
    def test_0_estrela_1_aceita_01(self):
        conversor = ConversorERparaAFN('0*1')
        afn = conversor.converter()
        reconhecedor = ReconhecedorAFN(afn)
        aceita, _ = reconhecedor.reconhecer('01')
        self.assertTrue(aceita)
    
    def test_0_estrela_1_aceita_0001(self):
        conversor = ConversorERparaAFN('0*1')
        afn = conversor.converter()
        reconhecedor = ReconhecedorAFN(afn)
        aceita, _ = reconhecedor.reconhecer('0001')
        self.assertTrue(aceita)
    
    def test_0_estrela_1_rejeita_0(self):
        conversor = ConversorERparaAFN('0*1')
        afn = conversor.converter()
        reconhecedor = ReconhecedorAFN(afn)
        aceita, _ = reconhecedor.reconhecer('0')
        self.assertFalse(aceita)


class TestReconhecimentoCadeiaLonga(unittest.TestCase):
    def setUp(self):
        Estado.contador = 0
    
    def test_a_estrela_aceita_10_as(self):
        conversor = ConversorERparaAFN('a*')
        afn = conversor.converter()
        reconhecedor = ReconhecedorAFN(afn)
        aceita, _ = reconhecedor.reconhecer('a' * 10)
        self.assertTrue(aceita)
    
    def test_a_ou_b_estrela_aceita_sequencia_longa(self):
        conversor = ConversorERparaAFN('(a|b)*')
        afn = conversor.converter()
        reconhecedor = ReconhecedorAFN(afn)
        aceita, _ = reconhecedor.reconhecer('ababbaabba')
        self.assertTrue(aceita)
    
    def test_0_ou_1_estrela_aceita_binario_longo(self):
        conversor = ConversorERparaAFN('(0|1)*')
        afn = conversor.converter()
        reconhecedor = ReconhecedorAFN(afn)
        aceita, _ = reconhecedor.reconhecer('110010110101')
        self.assertTrue(aceita)


class TestReconhecimentoPadrao(unittest.TestCase):
    def setUp(self):
        Estado.contador = 0
    
    def test_a_b_estrela_c_aceita_ac(self):
        conversor = ConversorERparaAFN('ab*c')
        afn = conversor.converter()
        reconhecedor = ReconhecedorAFN(afn)
        aceita, _ = reconhecedor.reconhecer('ac')
        self.assertTrue(aceita)
    
    def test_a_b_estrela_c_aceita_abc(self):
        conversor = ConversorERparaAFN('ab*c')
        afn = conversor.converter()
        reconhecedor = ReconhecedorAFN(afn)
        aceita, _ = reconhecedor.reconhecer('abc')
        self.assertTrue(aceita)
    
    def test_a_b_estrela_c_aceita_abbbc(self):
        conversor = ConversorERparaAFN('ab*c')
        afn = conversor.converter()
        reconhecedor = ReconhecedorAFN(afn)
        aceita, _ = reconhecedor.reconhecer('abbbc')
        self.assertTrue(aceita)
    
    def test_a_b_estrela_c_rejeita_a(self):
        conversor = ConversorERparaAFN('ab*c')
        afn = conversor.converter()
        reconhecedor = ReconhecedorAFN(afn)
        aceita, _ = reconhecedor.reconhecer('a')
        self.assertFalse(aceita)
    
    def test_a_b_estrela_c_rejeita_ab(self):
        conversor = ConversorERparaAFN('ab*c')
        afn = conversor.converter()
        reconhecedor = ReconhecedorAFN(afn)
        aceita, _ = reconhecedor.reconhecer('ab')
        self.assertFalse(aceita)


if __name__ == '__main__':
    unittest.main(verbosity=2)
