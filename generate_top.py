import random
import string
import os

# List of common first and last names
first_names = [
"James", "Mary", "Robert", "Patricia", "John", "Jennifer", "Michael", "Linda", 
"William", "Elizabeth", "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica", 
"Thomas", "Sarah", "Charles", "Karen", "Christopher", "Nancy", "Daniel", "Lisa", 
"Matthew", "Betty", "Anthony", "Sandra", "Donald", "Ashley", "Paul", "Kimberly", 
"Mark", "Donna", "George", "Emily", "Kenneth", "Helen", "Steven", "Deborah", 
"Edward", "Jessica", "Brian", "Sharon", "Ronald", "Cynthia", "Kevin", "Kathleen", 
"Jason", "Amy", "Jeffrey", "Angela", "Ryan", "Melissa", "Jacob", "Stephanie", 
"Gary", "Rebecca", "Nicholas", "Laura", "Eric", "Michelle", "Stephen", "Sophia", 
"Jonathan", "Evelyn", "Frank", "Hannah", "Larry", "Julie", "Scott", "Victoria", 
"Justin", "Kelly", "Brandon", "Christina", "Raymond", "Lauren", "Gregory", "Martha", 
"Joshua", "Judith", "Jerry", "Amanda", "Dennis", "Frances", "Walter", "Cheryl", 
"Patrick", "Megan", "Peter", "Andrea", "Harold", "Ann", "Douglas", "Alice", 
"Henry", "Marilyn", "Carl", "Heather", "Arthur", "Teresa", "Ryan", "Gloria", 
"Christian", "Kathryn", "Austin", "Debra", "Russell", "Janet", "Bryan", "Diane", 
"Bruce", "Rachel", "Lawrence", "Carol", "Jordan", "Emma", "Wayne", "Maria", 
"Dylan", "Joan", "Ralph", "Ella", "Eugene", "Julia", "Albert", "Victoria", 
"Jesse", "Amber", "Joe", "Danielle", "Logan", "Mildred", "Arthur", "Martha", 
"Sean", "Marlene", "Philip", "Jane", "Terry", "Joyce", "Gabriel", "Rita", 
"Harold", "Kathy", "Aaron", "Judith", "Alan", "Shirley", "Roy", "Brenda", 
"Nathan", "Pamela", "Carl", "Irene", "Ray", "Janice", "Shawn", "Maria", 
"Albert", "Sara", "Chris", "Ruby", "Patrick", "Carmen", "Jack", "Ellen", 
"Tony", "Annie", "Bobby", "Margaret", "Howard", "Daisy", "Larry", "Rose"
]
last_names = [
"Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis", "Garcia", 
"Rodriguez", "Wilson", "Martinez", "Anderson", "Taylor", "Thomas", "Hernandez", "Moore", 
"Martin", "Jackson", "Thompson", "White", "Lopez", "Lee", "Gonzalez", "Harris", 
"Clark", "Lewis", "Robinson", "Walker", "Perez", "Hall", "Young", "Allen", 
"Sanchez", "Wright", "King", "Scott", "Green", "Baker", "Adams", "Nelson", 
"Hill", "Ramirez", "Campbell", "Mitchell", "Roberts", "Carter", "Phillips", "Evans", 
"Turner", "Torres", "Parker", "Collins", "Edwards", "Stewart", "Flores", "Morris", 
"Nguyen", "Murphy", "Rivera", "Cook", "Rogers", "Morgan", "Peterson", "Cooper", 
"Reed", "Bailey", "Bell", "Gomez", "Kelly", "Howard", "Ward", "Cox", 
"Diaz", "Richardson", "Wood", "Watson", "Brooks", "Bennett", "Gray", "James", 
"Reyes", "Cruz", "Hughes", "Price", "Myers", "Long", "Foster", "Sanders", 
"Ross", "Morales", "Powell", "Sullivan", "Russell", "Ortiz", "Jenkins", "Gutierrez", 
"Perry", "Butler", "Barnes", "Fisher", "Henderson", "Coleman", "Simmons", "Patterson", 
"Jordan", "Reynolds", "Hamilton", "Graham", "Kim", "Gonzales", "Alexander", "Ramos", 
"Wallace", "Griffin", "West", "Cole", "Hayes", "Chavez", "Gibson", "Bryant", 
"Ellis", "Stevens", "Murray", "Ford", "Marshall", "Owens", "McDonald", "Harrison", 
"Ruiz", "Kennedy", "Wells", "Alvarez", "Woods", "Mendoza", "Castillo", "Olson", 
"Webb", "Washington", "Tucker", "Freeman", "Burns", "Henry", "Vasquez", "Snyder"
]

# Directory path
directory = "rop/NameRead"

# Ensure the directory exists
if not os.path.exists(directory):
    os.makedirs(directory)

# Helper function to generate a random name
def random_name():
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    return first_name, last_name

# Helper function to generate a random birthday in the format DDMMYYYY
def random_birthday():
    day = random.randint(1, 31)
    month = random.randint(1, 12)
    year = random.randint(1970, 2025)
    return f"{month:02d}{day:02d}{year}"

# Helper function to generate random phone numbers with +855 (Cambodia)
def generate_random_phone():
    phrandom = ['096', '097', '088', '071']
    random_phone = random.choice(phrandom)
    digit_phone = random.randint(1000000, 9999999)
    final_phone = random_phone + str(digit_phone)
    return final_phone

# Helper function to generate random passwords
def random_password(length=10):
    symbols = ['@', '#', '$', '%']
    symbol = random.choice(symbols)
    rand_part = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    number = str(random.randint(100, 999))
    return f"{symbol}{rand_part}{symbol}{number}"

# Write random data to files
def write_random_data():
    # Open the files for appending
    with open(os.path.join(directory, "name.txt"), 'w') as name_file, \
         open(os.path.join(directory, "birthday.txt"), 'w') as birthday_file, \
         open(os.path.join(directory, "phone.txt"), 'w') as phone_file, \
         open(os.path.join(directory, "Password.txt"), 'w') as password_file:
        
        # Generate and write random data 100 times
        for _ in range(1000):
            first_name, last_name = random_name()
            birthday = random_birthday()
            phone = generate_random_phone()
            password = random_password()

            # Write the data to the respective files
            name_file.write(f"{first_name}|{last_name}\n")
            birthday_file.write(f"{birthday[:2]}{birthday[2:4]}{birthday[4:]}\n")  # Format as DD/MM/YYYY
            phone_file.write(f"{phone}\n")
            password_file.write(f"{password}\n")

    print("100 random entries have been written to the files.")

write_random_data()
