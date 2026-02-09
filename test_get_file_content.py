from functions.get_file_content import get_file_content

def main():
    result = get_file_content("calculator", "lorem.txt")
    length_of_result = len(result)
    print(f"The length of the lorem ipsum is: {length_of_result}")

    result = get_file_content("calculator", "main.py")
    print(f"{result}")

    result = get_file_content("calculator", "pkg/calculator.py")
    print(f"{result}")

    result = get_file_content("calculator", "/bin/cat")
    print(f"{result}")

    result = get_file_content("calculator", "pkg/does_not_exist.py") 
    print(f"{result}")
    

if __name__ == "__main__":
    main()

