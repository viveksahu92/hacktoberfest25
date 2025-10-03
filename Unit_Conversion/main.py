conversions_length = {("meters", "feet"): 3.28084, ("feet", "meters"): 0.3048,
                      ("kilometers", "miles"): 0.621371, ("miles", "kilometers"): 1.60934,
                      ("centimeters", "inches"): 0.393701, ("inches", "centimeters"): 2.54,
                      ("meters", "miles"): 0.000621371, ("miles", "meters"): 1609.34,
                      ("meters", "inches"): 39.3701, ("inches", "meters"): 0.0254,
                      ("yards", "meters"): 0.9144, ("meters", "yards"): 1.09361,
                      ("meters", "kilometers"): 0.001, ("kilometers", "meters"): 1000,
                      ("feet", "miles"): 0.000189394, ("miles", "feet"): 5280,
                      ("meters", "centimeters"): 100, ("centimeters", "meters"): 0.01,
                      ("inches", "feet"): 0.0833333, ("feet", "inches"): 12,
                      ("yards", "feet"): 3, ("feet", "yards"): 0.333333,("kilometers","yards"):1093.61,
                      ("yards","kilometers"):0.0009144,("meters","milimeters"):1000,("milimeters","meters"):0.001,
                      ("centimeters","milimeters"):10,("milimeters","centimeters"):0.1,
                      ("inches","milimeters"):25.4,("milimeters","inches"):0.0393701,
                      ("miles","yards"):1760,("yards","miles"):0.000568182,
                      ("kilometers","feet"):3280.84,("feet","kilometers"):0.0003048,
                      ("kilometers","centimeters"):100000,("centimeters","kilometers"):0.00001,
                      ("miles","inches"):63360,("inches","miles"):0.0000157828,
                      ("miles","milimeters"):1609344,("milimeters","miles"):0.000000621371,
                      ("yards","centimeters"):91.44,("centimeters","yards"):0.0109361,
                      ("yards","inches"):36,("inches","yards"):0.0277778,
                      ("feet","centimeters"):30.48,("centimeters","feet"):0.0328084,
                      ("feet","milimeters"):304.8,("milimeters","feet"):0.00328084,
                      ("inches","centimeters"):2.54,("centimeters","inches"):0.393701,
                      ("kilometers","milimeters"):1000000,("milimeters","kilometers"):0.000001,
                      ("kilometers","inches"):39370.1,("inches","kilometers"):0.0000254,
                      ("miles","centimeters"):160934,("centimeters","miles"):0.00000621371,
                      ("yards","milimeters"):914.4,("milimeters","yards"):0.00109361}


conversions_weight = {("kilograms", "pounds"): 2.20462, ("pounds", "kilograms"): 0.453592,
                      ("grams", "ounces"): 0.035274, ("ounces", "grams"): 28.3495,
                      ("stones", "pounds"): 14, ("pounds", "stones"): 0.0714286,
                      ("kilograms", "grams"): 1000, ("grams", "kilograms"): 0.001,
                      ("kilograms", "ounces"): 35.274, ("ounces", "kilograms"): 0.0283495,
                      ("kilograms", "stones"): 0.157, ("stones", "kilograms"): 6.35029,
                      ("grams", "pounds"): 0.00220462, ("pounds","grams"):453.592,
                      ("grams","stones"):0.000157473,("stones","grams"):6350.29,
                      ("ounces","pounds"):0.0625,("pounds","ounces"):16,
                      ("ounces","stones"):0.00446429,("stones","ounces"):224,
                      ("miligrams","grams"):0.001,("grams","miligrams"):1000,
                      ("miligrams","kilograms"):0.000001,("kilograms","miligrams"):1000000,
                      ("miligrams","pounds"):0.00000220462,("pounds","miligrams"):453592,
                      ("miligrams","ounces"):0.000035274,("ounces","miligrams"):28349.5,
                      ("miligrams","stones"):0.000157473,("stones","miligrams"):6350.29}


print("Welcome to the Unit Conversion Tool!")            
               
while True:
    print("Select the type of conversion:")
    print("1. Length")
    print("2. Weight")
    print("3. Exit")
    choice = input("Enter your choice: ")
    
    if choice == '1':
        print("Available conversions: meters, feet, kilometers, miles, centimeters, inches, yards, milimeters")
        from_unit = input("Convert from: ").lower()
        to_unit = input("Convert to: ").lower()
        if (from_unit, to_unit) in conversions_length:
            value = float(input(f"Enter value in {from_unit}: "))
            converted_value = value * conversions_length[(from_unit, to_unit)]
            print(f"{value} {from_unit} is equal to {converted_value} {to_unit}")
        else:
            print("Conversion not supported.")
            
    elif choice == '2':
        print("Available conversions: kilograms, pounds, grams, ounces, stones, miligrams")
        from_unit = input("Convert from: ").lower()
        to_unit = input("Convert to: ").lower()
        if (from_unit, to_unit) in conversions_weight:
            value = float(input(f"Enter value in {from_unit}: "))
            converted_value = value * conversions_weight[(from_unit, to_unit)]
            print(f"{value} {from_unit} is equal to {converted_value} {to_unit}")
        else:
            print("Conversion not supported.")
            
    elif choice == '3':
        print("Thank you for using the Unit Conversion Tool!")
        break
    
    else:
        print("Invalid choice. Please try again.")
        