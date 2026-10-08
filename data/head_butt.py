"""DCOR - Head Butt como item (03/10, Neitan): a cabeçada só sai com o talismã Skull EQUIPADO, e as gárgulas (Earth,
Water, Air) também dão cabeçada com Cima + A, no chão e no ar, como a Infinity do jogo original.

Jogo original: a cabeçada é da forma normal do Firebrand. Habilidades por forma em $81:B2EB (copiada em $1003 por
80:DF98): Firebrand 07, Tidal 08, Aerial 21, Ground 12, Legendary 07, Infinity 3F; bit 04 = cabeçada, 08 = nado da
Tidal, 10 = A da Ground (investida), 20 = A da Aerial, 01 = plana/voa (estado 06). Estados do Firebrand ($1005, tabela
80:E002): 02 chão, 04 pulo/queda, 06 planando/voando, 0A cabeçada, 12 cabeçada no ar, 14 nadando, 16 A da Ground, 1A A
da Aerial. Entradas da cabeçada (todas com LDA $03 / AND #$04 / BEQ sai):
  80:F1B3  chão (estado 02, via 80:F181)            -> JMP 80:E157 (estado 0A)
  80:F1C2  pulo/queda (estado 04, via 80:F1BE)      -> JMP 80:E1A3 (estado 12, vira 0A ao aterrissar em 80:E517)
  80:E7FD  nadando (estado 14): só com A + Cima     -> JMP 80:E1A3
No chão, 80:F181 manda o A da forma com o bit 10 (Ground, Infinity) pra habilidade dela (80:F1A4, estado 16), menos na
Infinity com Cima ($02 = forma × 2 = 0A e $0091 & 08, 80:F18C-F197), que vai pra 80:F1B3: é o "Cima + A". Voando
(estado 06), o A só vai pra habilidade da Aerial (80:F1CD, bit 20); lá não existe cabeçada.

Com a opção:
  - as 3 entradas viram JSL 'check': pode = Skull equipada E (bit 04 da forma OU Cima segurado). Firebrand normal:
    A puro, como sempre; gárgulas: Cima + A;
  - 80:F18C (LDA $02 / CMP #$0A, antes do BNE pra habilidade): 'ground' segue o caminho da Infinity também com a Skull
    equipada e Cima segurado (a Ground dá cabeçada com Cima + A; sem Cima, a investida de sempre);
  - 80:F1D1 (LDA $03 / AND #$20 do A voando): 'hover' faz a cabeçada no ar com Skull + Cima nas formas sem o bit 04
    (Aerial); o resto segue pra habilidade da Aerial como sempre (o Firebrand normal planando continua sem cabeçada).
Objetos que reagem à cabeçada (Neitan, 04/10: a Ground com a Skull não acordava a estátua do Hippogriff 1): 80:9FFA
(estátua do Hippogriff 82:9B21, 82:A125, 84:CD1E) e 80:9FC5 (82:CA0F, BE:F980) só aceitam a forma com o bit 04
($1003, 80:9FFC / 80:9FC7) e a animação 10 ou 16 ($100D, 80:9FE2) no 3º passo com o contador em 0E (80:9FD4). Com a
opção: 'obj_check' = Skull equipada; 'obj_anim' = a animação de cabeçada da forma (Firebrand normal, Legendary e Infinity:
10/16; cada gárgula: só a animação nova dela, porque a animação 10 da Aerial também passa pelo 3º passo com 0E e
acordaria estátuas andando). O tempo da animação nova é o do Firebrand, então o 3º passo com 0E bate.
Talismã equipado = $1066, posição no menu (contador começa em 3, 84:8FF7: posição k -> 2(k+1)): Crown 28, Skull 2A,
Armor 2C, Fang 2E (a Fang dobra o dano com $1066 = 2E, 82:8820), Hand 30. O efeito original da Skull continua.

Animação da cabeçada nas gárgulas (passo 4 do Neitan, adiantado: sem ela o Firebrand ficava preso no estado 0A).
Os estados 0A/12 usam as ações 10/16 da tabela de ações da forma ($81:B19F[forma] -> [animação][lista]); o estado 0A
quebra o quebrável quando o contador do passo está em 10 ($0E, 80:E53A) e acaba quando a animação chega no 5º passo
($0F = 08, 80:E54D). Firebrand normal: animação 10 = (12, q25) (4, q26) (16, q27) (9, q26) (9, q26). Nas gárgulas as
ações 10/16 apontam pra animação 00 (parado, em laço) com a lista 10 do Firebrand normal: nunca acabava. Agora cada
gárgula ganha uma animação de 5 passos no tempo do Firebrand com 2 quadros dela (Neitan, 04/10): o quadro 1 na preparação e o
quadro de frente (o de entrar em portas) no golpe e até o fim; e uma lista com os tiles desses quadros:
  - animação: bloco por sprite, sem compressão ([tamanho u16][tabela de deslocamentos][passos (duração, quadro); 00 +
    passo de volta]); 80:DA79 lê o deslocamento em $8E:C000 + sprite × 2 e copia o bloco pra $7F (que guarda a posição
    de cada sprite em $0980). Gancho em 80:DA80: os sprites 66/67/68 vêm de cópias nossas em C3:9000+ com uma
    animação a mais no fim da tabela (os deslocamentos antigos andam 2);
  - lista: 1 palavra por PASSO (80:F8A2 usa $0F), registro de DMA dos tiles (bits 13-15 = banco $9A+, resto = registro
    de 12 B em $98:B000). Lida no banco $81 (DB do código): os ids novos F0/F2/F4 são copiados pra RAM baixa
    ($1EC0, livre; o banco $81 enxerga a RAM em $0000-$1FFF) pelo gancho em 80:F88D, que aponta $18 pra lá.
De onde vem o registro de cada quadro: mapa de sprites do editor (`DemonsCrest Editor/sprites_png/*_layout.json`,
campo "fonte", 03/10). Quadros escolhidos pelo Neitan (04/10): Tidal q1 / q30, Aerial q1 / q33, Ground q1 / q19
(no Ground ele passou o registro 45D0, que é o do q14; o do q1 é 454C).
"""
from asm65816 import Asm

BASE = 0xC38000
SKULL = 0x2A                 # $1066 com a Skull equipada
EQUIPPED = 0x7E1066
PAD_HI = 0x7E0091            # botões (byte alto): 08 = Cima
SITES = (0x80F1B3, 0x80F1C2, 0x80E7FD)   # LDA $03 / AND #$04 (A 8 bits), seguidos de BEQ (sem cabeçada)
STEPS = ((12, 0), (4, 0), (16, 1), (9, 1), (9, 1))   # (duração, quadro: 0 = inicial, 1 = final): o tempo do Firebrand
LIST_RAM = 0x1EC0            # lista da cabeçada da gárgula atual (16 B)
ANIM_BASE = 0xC39000         # blocos de animação das gárgulas (0x100 cada)
FORM = {0x66: 0x02, 0x67: 0x04, 0x68: 0x06}     # sprite -> $1002 (forma × 2) da gárgula
# sprite: (nome, tabela de ações, quadros inicial/final, registro de DMA de cada um, id da lista nova)
GARGOYLES = {0x66: ('Tidal', 0x81B1EB, (1, 30), (0x227C, 0x23B4), 0xF0),
             0x67: ('Aerial', 0x81B26B, (1, 33), (0x23CC, 0x451C), 0xF2),
             0x68: ('Ground', 0x81B22B, (1, 19), (0x454C, 0x4540), 0xF4)}


def anim_block(rom, sid, frames):
    """Bloco de animação do sprite com a cabeçada no fim: (bytes do bloco, índice da animação nova)."""
    lo = rom.u16(0x8EC000 + sid * 2)                       # como 80:DA80
    y = lo + 0xC000
    bank = 0x8E + (y > 0xFFFF)
    p = bank << 16 | ((y & 0xFFFF) | (0xC000 if y > 0xFFFF else 0))
    n = rom.u16(p)
    data = bytes(rom.b[rom.off(p) + 2 + i] for i in range(n))
    first = min(data[i] | data[i + 1] << 8 for i in range(0, data[0] | data[1] << 8, 2))
    table = [data[i] | data[i + 1] << 8 for i in range(0, first, 2)]
    new = b''.join((o + 2).to_bytes(2, 'little') for o in table) + (n + 2).to_bytes(2, 'little')
    new += data[first:] + bytes(b for d, k in STEPS for b in (d, frames[k])) + b'\x00\x04'
    assert len(new) + 2 <= 0x100 and first < 0xF0
    return len(new).to_bytes(2, 'little') + new, first


def apply(rom):
    """rom: insanity_rom.Rom (4 MB). Devolve linhas de relatório."""
    anims = {sid: anim_block(rom, sid, GARGOYLES[sid][2]) for sid in GARGOYLES}   # (bloco, índice da animação)
    a = Asm(BASE)
    # Tudo com A/X 8 bits (as rotinas do Firebrand rodam com SEP #$30).
    # check: Z = 0 pode (como o AND #$04 original com o bit ligado), Z = 1 não pode (o BEQ seguinte pula)
    a.label('check')
    a.op('LDA', 'long', EQUIPPED); a.op('CMP', 'imm8', SKULL); a.br('BNE', 'no')
    a.op('LDA', 'dp', 0x03); a.op('AND', 'imm8', 0x04); a.br('BNE', 'out')      # forma com cabeçada: A puro
    a.op('LDA', 'long', PAD_HI); a.op('AND', 'imm8', 0x08)                     # gárgula: só com Cima
    a.op('RTL')
    a.label('no')
    a.op('LDA', 'imm8', 0x00)
    a.label('out')
    a.op('RTL')
    # ground: no lugar de LDA $02 / CMP #$0A (o BNE seguinte vai pra habilidade). Z = 1 = caminho da Infinity
    a.label('ground')
    a.op('LDA', 'dp', 0x02); a.op('CMP', 'imm8', 0x0A); a.br('BEQ', 'g_out')    # Infinity: como sempre
    a.op('LDA', 'long', EQUIPPED); a.op('CMP', 'imm8', SKULL); a.br('BNE', 'g_out')   # Z = 0: habilidade
    a.op('LDA', 'long', PAD_HI); a.op('AND', 'imm8', 0x08); a.op('EOR', 'imm8', 0x08)  # Cima: Z = 1
    a.label('g_out')
    a.op('RTL')
    # hover: no lugar de LDA $03 / AND #$20 (A apertado, voando; o BEQ seguinte volta sem nada)
    a.label('hover')
    a.op('LDA', 'dp', 0x03); a.op('AND', 'imm8', 0x04); a.br('BNE', 'h_ab')     # forma com cabeçada: como sempre
    a.op('LDA', 'long', EQUIPPED); a.op('CMP', 'imm8', SKULL); a.br('BNE', 'h_ab')
    a.op('LDA', 'long', PAD_HI); a.op('AND', 'imm8', 0x08); a.br('BEQ', 'h_ab')
    a.op('PLA'); a.op('PLA'); a.op('PLA')                                      # volta do JSL
    a.op('PLA'); a.op('PLA')                                                   # e do JSR 80:F1CD (como 80:F1C8)
    a.op('JML', 'long', 0x80E1A3)                                              # cabeçada no ar
    a.label('h_ab')
    a.op('LDA', 'dp', 0x03); a.op('AND', 'imm8', 0x20)                         # o original
    a.op('RTL')
    # anim_src: no lugar de 80:DA80-DA95 (A/X 16 bits, X = sprite × 2): Y = endereço do bloco, $12 = banco
    a.label('anim_src')
    for k, sid in enumerate(sorted(GARGOYLES)):
        a.op('CPX', 'imm16', sid * 2); a.br('BEQ', f'as{k}')
    a.op('LDA', 'longx', 0x8EC000); a.op('CLC'); a.op('ADC', 'imm16', 0xC000); a.br('BCC', 'as_c')   # o original
    a.op('ORA', 'imm16', 0xC000)
    a.label('as_c')
    a.op('TAY'); a.op('LDA', 'imm16', 0x008E); a.op('ADC', 'imm16', 0x0000); a.op('STA', 'dp', 0x12)
    a.op('RTL')
    for k, sid in enumerate(sorted(GARGOYLES)):
        a.label(f'as{k}')
        a.op('LDY', 'imm16', (ANIM_BASE + 0x100 * k) & 0xFFFF); a.br('BRA', 'as_set')
    a.label('as_set')
    a.op('LDA', 'imm16', ANIM_BASE >> 16); a.op('STA', 'dp', 0x12)
    a.op('RTL')
    # list_src: no lugar de 80:F88D-F896 (A/X/Y 8 bits, Y = id da lista): $18/$19 = ponteiro da lista (banco $81)
    a.label('list_src')
    a.op('CPY', 'imm8', 0xF0); a.br('BCS', 'ls_new')
    a.op('LDA', 'absy', 0xB7EC); a.op('STA', 'dp', 0x18); a.op('LDA', 'absy', 0xB7ED); a.op('STA', 'dp', 0x19)
    a.op('RTL')
    a.label('ls_new')
    a.op('PHX'); a.op('PHY')
    a.op('TYA'); a.op('SEC'); a.op('SBC', 'imm8', 0xF0); a.op('ASL', 'acc'); a.op('ASL', 'acc'); a.op('ASL', 'acc')
    a.op('TAX'); a.op('LDY', 'imm8', 0x00)
    a.label('ls_copy')                                                         # 16 B da lista -> $1EC0 (RAM baixa)
    a.op('LDA', 'longx', 'lists'); a.op('STA', 'absy', LIST_RAM); a.op('INX'); a.op('INY')
    a.op('CPY', 'imm8', 0x10); a.br('BNE', 'ls_copy')
    a.op('LDA', 'imm8', LIST_RAM & 0xFF); a.op('STA', 'dp', 0x18)
    a.op('LDA', 'imm8', LIST_RAM >> 8); a.op('STA', 'dp', 0x19)
    a.op('PLY'); a.op('PLX')
    a.op('RTL')
    # obj_check: no lugar de LDA $1003 / AND #$04 em 80:9FC7 e 80:9FFC (o BEQ seguinte = não acertou)
    a.label('obj_check')
    a.op('LDA', 'long', EQUIPPED); a.op('CMP', 'imm8', SKULL); a.br('BNE', 'oc_no')
    a.op('LDA', 'imm8', 0x04); a.op('RTL')                                     # Z = 0
    a.label('oc_no')
    a.op('LDA', 'imm8', 0x00); a.op('RTL')                                     # Z = 1
    # obj_anim: no lugar de 80:9FE2 (animação $100D = 10 ou 16): Z = 1 = animação de cabeçada da forma
    a.label('obj_anim')
    a.op('LDA', 'long', 0x7E1002)
    for k, sid in enumerate(sorted(GARGOYLES)):
        a.op('CMP', 'imm8', FORM[sid]); a.br('BEQ', f'oa{k}')
    a.op('LDA', 'long', 0x7E100D); a.op('CMP', 'imm8', 0x10); a.br('BEQ', 'oa_out')   # as outras formas: como
    a.op('CMP', 'imm8', 0x16)                                                          # no original
    a.label('oa_out')
    a.op('RTL')
    for k, sid in enumerate(sorted(GARGOYLES)):
        a.label(f'oa{k}')
        a.op('LDA', 'long', 0x7E100D); a.op('CMP', 'imm8', anims[sid][1]); a.op('RTL')
    a.label('lists')
    for sid in sorted(GARGOYLES):
        recs = GARGOYLES[sid][3]
        a.b += b''.join(recs[k].to_bytes(2, 'little') for _, k in STEPS) + bytes(6)
    code = a.resolve()
    L = a.labels
    o = rom.off(BASE)
    assert not any(rom.b[o:o + len(code)]), 'banco $C3 não está vazio'
    rom.put(BASE, code)
    jsl = lambda lab: bytes((0x22,)) + L[lab].to_bytes(3, 'little')
    for addr in SITES:
        rom.expect(addr, bytes.fromhex('a5032904'))
        rom.put(addr, jsl('check'))
    rom.expect(0x80F18C, bytes.fromhex('a502c90ad012'))
    rom.put(0x80F18C, jsl('ground'))                                           # o BNE $F1A4 em 80:F190 fica
    rom.expect(0x80F1D1, bytes.fromhex('a5032920f0ae'))
    rom.put(0x80F1D1, jsl('hover'))                                            # o BEQ $F185 em 80:F1D5 fica
    # animação e lista das gárgulas
    rom.expect(0x80DA80, bytes.fromhex('bf00c08e186900c090030900c0a8a98e006900008512'))
    rom.put(0x80DA80, jsl('anim_src') + bytes.fromhex('8010') + b'\xEA' * 16)   # BRA pra 80:DA96
    rom.expect(0x80F88D, bytes.fromhex('b9ecb78518b9edb78519'))
    rom.put(0x80F88D, jsl('list_src') + b'\xEA' * 6)                           # o JSR 80:F89B / RTL ficam
    # objetos que reagem à cabeçada
    for addr in (0x809FC7, 0x809FFC):
        rom.expect(addr, bytes.fromhex('ad03102904'))
        rom.put(addr, jsl('obj_check') + b'\xEA')                             # o BEQ 80:9FF8 seguinte fica
    rom.expect(0x809FE2, bytes.fromhex('ad0d10c910f007ad0d10c916d008'))
    rom.put(0x809FE2, jsl('obj_anim') + bytes.fromhex('d010') + bytes.fromhex('8006') + b'\xEA' * 4)   # BNE 9FF8 /
    report = []
    for k, sid in enumerate(sorted(GARGOYLES)):
        name, table, frames, _, list_id = GARGOYLES[sid]
        block, anim = anims[sid]                                               # BRA 9FF0 (acertou)
        at = ANIM_BASE + 0x100 * k
        assert not any(rom.b[rom.off(at):rom.off(at) + 0x100])
        rom.put(at, block)
        for action in (0x10, 0x16):                                            # cabeçada no chão e no ar
            rom.put(table + action, bytes((anim, list_id)))
        report.append(f'{name}: animação {anim:02X} (quadros {frames[0]} e {frames[1]}), lista {list_id:02X}')
    return [f'head butt: só com a Skull equipada ($1066 = {SKULL:02X}); gárgulas com Cima + A; ganchos 80:F1B3, '
            f'80:F1C2, 80:E7FD, 80:F18C, 80:F1D1, 80:DA80, 80:F88D, 80:9FC7, 80:9FFC, 80:9FE2; código {BASE >> 16:02X}:{BASE & 0xFFFF:04X}-'
            f'{(BASE + len(code) - 1) & 0xFFFF:04X}'] + report
