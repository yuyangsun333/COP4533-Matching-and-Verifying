def data_reader(file_path):
    """
    Read the input data and return as 
        n: number of hospitals/students
        hostial preferences list
        student preferences list
    """
    with open(file_path, 'r') as file:
        data = file.readlines()
    
    # Remove any trailing newlines and spaces
    data = [line.strip() for line in data if line.strip()]

    if not data:
        raise ValueError("Input file is empty or improperly formatted.")

    n = int(data[0])
    hospital_prefs = []
    student_prefs = []

    for i in range(1, n + 1):
        prefs = list(map(int, data[i].split()))
        hospital_prefs.append(prefs)

    for i in range(n + 1, 2 * n + 1):
        prefs = list(map(int, data[i].split()))
        student_prefs.append(prefs)

    return n, hospital_prefs, student_prefs

print(data_reader('data/example.in'))