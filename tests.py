from functions.run_python_file import run_python_file

def main():
    a = run_python_file("calculator", "main.py")
    b = run_python_file("calculator", "main.py", ["3 + 5"])
    c = run_python_file("calculator", "tests.py")
    d = run_python_file("calculator", "../main.py")
    f = run_python_file("calculator", "nonexistent.py")

    print("---A---")
    print(a)
    print("---B---")
    print(b)
    print("---C---")
    print(c)
    print("---D---")
    print(d)
    print("---F---")
    print(f)


if __name__ == "__main__":
    main()