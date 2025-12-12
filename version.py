import subprocess

# 读取原 requirements 文件
with open("requirements.txt", "r") as f:
    packages = [line.strip() for line in f if line.strip() and not line.startswith("#")]

# 获取当前环境安装的所有包及版本
# 使用 pip list --format=freeze 更稳健
installed = subprocess.check_output(["pip", "list", "--format=freeze"], text=True)
installed_dict = {}
for line in installed.splitlines():
    if "==" in line:
        pkg, version = line.split("==")
        installed_dict[pkg.lower()] = version

# 生成带版本号的 requirements 文件
with open("requirements_with_versions.txt", "w") as f:
    for pkg in packages:
        pkg_lower = pkg.lower().replace("_", "-")  # 兼容 PyPI 名称
        version = installed_dict.get(pkg_lower) or installed_dict.get(pkg_lower.replace("-", "_"))
        if version:
            f.write(f"{pkg}=={version}\n")
        else:
            f.write(f"{pkg}\n")  # 没安装就保留原名

print("已生成 requirements_with_versions.txt")
