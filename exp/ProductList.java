//exp1
import java.util.Scanner;

public class ProductList{
    public static void main(String[] args) {
        String name;
        int Quantity;
        double price;
        int gst;
        int id;
        try(Scanner sc=new Scanner(System.in))
    {
        System.out.println("Enter the name of product:");
        name=sc.nextLine();
        System.out.println("Enter the Quantity of product:");
        Quantity=sc.nextInt();
        System.out.println("Enter the price of product:");
        price=sc.nextDouble();
        System.out.println("Enter the gst of product:");
        gst=sc.nextInt();
        System.out.println("Enter the id of product:");
        id=sc.nextInt();
        sc.nextLine();

        //calculate gst
        double tax=(gst*price)/100;
        //final price
        double finalPrice=price+tax;

        //display the information
        System.out.println("The name s:"+name);
        System.out.println("The id s:"+id);
        System.out.println("The Quantity s:"+Quantity);
        System.out.println("The price s:"+price);
        System.out.println("The finalPrice s:"+finalPrice);

        if(finalPrice>500)
        {
            System.out.println("Expensive");
        }
        else{
            System.out.println("Not so expensive");
        }
        


    }
        

    }
}