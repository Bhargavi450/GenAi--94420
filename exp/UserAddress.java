// exp 4
// Program to create user and address class

import java.time.LocalDate;
import java.util.Scanner;

// User class
class User {
    String fName, lName, mName, email, mobile;
    LocalDate birthdate;

    // constructor
    public User(Scanner sc) {
        System.out.println("Enter your first name: ");
        this.fName = sc.nextLine();
        System.out.println("Enter your last name: ");
        this.lName = sc.nextLine();
        System.out.println("Enter your middle name: ");
        this.mName = sc.nextLine();
        System.out.println("Enter date of birth (YYYY MM DD): ");
        this.birthdate = LocalDate.of(sc.nextInt(), sc.nextInt(), sc.nextInt());
        sc.nextLine();
        System.out.println("Enter email: ");
        this.email = sc.nextLine();
        System.out.println("Enter mobile number: ");
        this.mobile = sc.nextLine();
        
    }

    public void displayUserInfo() {
        System.out.println("\nUser Info");
        System.out.println("First name: " + fName);
        System.out.println("Last name: " + lName);
        System.out.println("Middle name: " + mName);
        System.out.println("Birthdate: " + birthdate);
        System.out.println("Email: " + email);
        System.out.println("Mobile number: " + mobile);
    }
}

// Address class
class Address {
    String building, street, city, district, state, pin;

    // constructor
    public Address(Scanner sc) {
        System.out.println("\nEnter building: ");
        this.building = sc.nextLine();
        System.out.println("Enter street: ");
        this.street = sc.nextLine();
        System.out.println("Enter city: ");
        this.city = sc.nextLine();
        System.out.println("Enter district: ");
        this.district = sc.nextLine();
        System.out.println("Enter state: ");
        this.state = sc.nextLine();
        System.out.println("Enter pin: ");
        this.pin = sc.nextLine();
    }

    public void displayAddress() {
        System.out.println("\nAddress Info");
        System.out.println(building + " building, " + street + " street,");
        System.out.println(city + " city, district: " + district);
        System.out.println("State: " + state + " - " + pin);
    }
}

// Main Application class
public class Application {
    public static void main(String[] args) {
        try (Scanner sc = new Scanner(System.in)) {
            User user = new User(sc);
            user.displayUserInfo();
            
            Address address = new Address(sc);
            address.displayAddress();
        }
    }
}