import glob
import os

for file in glob.glob('../original/verilog/*.v'):
	name = os.path.basename(file)
	with open(file, 'r') as r:
		with open(name, 'w') as w:
			write = True
			for line in r:
				# fpu.v: co -> co_d
				if '// carry output' in line:
					line = line.replace('co', 'co_d')

				# fpu.v: missing fasu_op
				if 'nan_sign_d, result_zero_sign_d' in line:
					w.write('wire\t\tfasu_op;\n')

				# casex -> casez
				line = line.replace('casex(', 'casez(')

				# remove redundant <= #1
				line = line.replace('<= #1', '<=')

				if 'synopsys translate_off' in line:
					write = False
				if write:
					w.write(line)
				if 'synopsys translate_on' in line:
					write = True
	os.system(f'diff -u {file} {name} > ../{name}.diff')