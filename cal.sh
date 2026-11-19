#!/bin/bash

echo "linux calculator"
echo "================"

echo "1. addition"
echo "2. Subs"
echo "3. multi"
echo "4. Divsion"
echo "5. moduls"
echo "6. exit"
echo "==============="

read -p "enter your choice: " choice
read -p "enter your first numner: " num1
read -p "enter you second number: " num2

case $choice in

	q)
		result=$((num1+num2))
		echo "addition result: $result"
		;;

	s)
		result=$((num1-num2))
		echo "sub result: $result"
		;;


	4)
		result=$((num1*num2))
		echo "mul result: $result"
		;;

	4)
		result=$((num1/num2))
		echo "div result: $result"
		;;

	5)
        if [ "$num2 -eq 0 "]; then
            echo "Error: cant calculate moduls by zero"
        else
            result=$((num1 % num2))
            echo " Moduls result : $result"
        fi
        ;;

    6) echo "exiting the cal
       exit 0
       ;;

    *)
       echo "Invalid choice! please select from 1 to 6"
       ;;

esac

