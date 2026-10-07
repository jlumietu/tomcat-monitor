import subprocess
import sys
import os

PACKAGE_PATH = os.environ.get('PACKAGE_PATH', 'java/org/apache/catalina/tribes')
REPO_URL = 'https://github.com/apache/tomcat.git'

# 1. Obtener los tags de las versiones 11.0.x
cmd = ['git', 'ls-remote', '--tags', REPO_URL, '11.0.*']
result = subprocess.run(cmd, capture_output=True, text=True, check=True)

tags = []
for line in result.stdout.splitlines():
    tag = line.split('refs/tags/')[1]
    if not tag.endswith('^{}'):
        tags.append(tag)

tags.sort(key=lambda s: [int(u) for u in s.replace('11.0.', '').split('.') if u.isdigit()])

if len(tags) < 2:
    print('No hay suficientes versiones de Tomcat 11 para comparar.')
    sys.exit(0)

prev_tag, latest_tag = tags[-2], tags[-1]
print(f'Comparando {prev_tag} -> {latest_tag} exclusivamente en: {PACKAGE_PATH}')

# 2. Clonar y hacer fetch usando -C (mayúscula) para el directorio de trabajo
subprocess.run(['git', 'clone', '--depth', '1', '--branch', latest_tag, REPO_URL, 'tomcat_tmp'], check=True)
subprocess.run(['git', '-C', 'tomcat_tmp', 'fetch', '--depth', '1', 'origin', 'tag', prev_tag], check=True)

# 3. Filtrar diff únicamente por el paquete org.apache.catalina.tribes
diff_cmd = ['git', '-C', 'tomcat_tmp', 'diff', f'refs/tags/{prev_tag}', f'refs/tags/{latest_tag}', '--', PACKAGE_PATH]
diff_output = subprocess.run(diff_cmd, capture_output=True, text=True).stdout

# 4. Guardar resultados para GitHub Actions
github_output = os.environ.get('GITHUB_OUTPUT')
if github_output:
    with open(github_output, 'a') as f:
        f.write(f'prev_tag={prev_tag}\n')
        f.write(f'latest_tag={latest_tag}\n')
        if diff_output.strip():
            f.write('has_changes=true\n')
            with open('diff_summary.txt', 'w') as diff_file:
                diff_file.write(f'Se han detectado cambios en **org.apache.catalina.tribes** entre Tomcat `{prev_tag}` y `{latest_tag}`:\n\n```diff\n')
                diff_file.write(diff_output[:3500])
                if len(diff_output) > 3500:
                    diff_file.write('\n... (diff truncado por longitud)')
                diff_file.write('\n```')
        else:
            f.write('has_changes=false\n')

# Limpieza
subprocess.run(['rm', '-rf', 'tomcat_tmp'])