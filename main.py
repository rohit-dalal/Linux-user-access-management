import subprocess
import getpass
from os import system
from colorama import Fore


def options():
    # actions to perform
    return (
        Fore.GREEN
        + """
<<------------------------------------------------------------>>
            1. Add user             4. List users

            2. Modify user          5. Delete user

            3. Sudo action

                    6. exit or ctrl + c

    
                     _____________________
                    | Github: rohit-dalal |
                    |____check it out_____|
<<------------------------------------------------------------>>
            """
    )


def add(name, pass_):
    # Create a subprocess object to run the 'useradd' command
    p = subprocess.Popen(
        ["sudo", "-S", "useradd", name, "-p", pass_, "-s", "/bin/bash"],
        stdin=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )

    # get password and send to the subprocess
    sudo_password = getpass.getpass(prompt="[sudo]: sudo password: ")
    stderr, stdout = p.communicate(sudo_password + "\n")

    # check the error message if any error found
    if p.returncode != 0:
        print(Fore.RED + f"[!] :{stdout}!")

    else:
        print(Fore.GREEN + f"[+] {name}: user created successfully")


def delete(name):
    # Create a subprocess object to run the 'useradd' command
    p = subprocess.Popen(
        ["sudo", "-S", "userdel", name],
        stdin=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )

    # get password and send to the subprocess
    sudo_password = getpass.getpass(prompt="[sudo]: sudo password: ")
    stderr, stdout = p.communicate(sudo_password + "\n")

    # check the error message if any error foundd
    if p.returncode != 0:
        print(Fore.RED + f"[!] :{stdout}!")

    else:
        print(Fore.GREEN + f"[+] {name}: user deleted successfully.")


def users_list():
    # print all users in the system
    print(system("awk '{print NR\" \" $1}' /etc/passwd"))


def modify():
    # Create a subprocess object to run the 'useradd' command
    print(
        """
            1. Change user name
            2. Change password
    """
    )

    m_input = int(input("[modify]: Enter your command: "))

    # check input
    if m_input == 1:
        m_name = input("[modify]: Enter old user name: ")
        new_user_name = input("[modify]: Enter new user name: ")

        # Create a subprocess object to run the 'usermod' command
        p = subprocess.Popen(
            ["sudo", "-S", "usermod", "-l", new_user_name, m_name],
            stdin=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )

        # get password and send to the subprocess
        sudo_password = getpass.getpass(prompt="[sudo]: sudo password: ")
        stderr, stdout = p.communicate(sudo_password + "\n")

        # check the error message if any error found
        if p.returncode != 0:
            print(Fore.YELLOW + f"[-] :{stdout}!")

        else:
            print(Fore.GREEN + f"[+] {m_name}: user name changed successfully.")

    elif m_input == 2:
        m_input = str(input("[modify]: Enter user name: "))
        new_password = str(getpass.getpass(prompt="[modify]: Enter new password: "))

        # Create a subprocess object to run the 'passwd' command
        p = subprocess.Popen(
            ["sudo", "-S", "passwd", m_input, "-q"],
            stdin=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
            universal_newlines=True,
        )

        # get password and send to the subprocess
        sudo_password = getpass.getpass(prompt="[sudo]: sudo password: ")
        stderr, stdout = p.communicate(
            new_password + "\n" + new_password + "\n" + sudo_password
        )

        # check the error message if any error found
        if p.returncode != 0:
            print(Fore.RED + f"[!]: {stdout}!")
        else:
            print(Fore.GREEN + f"[+] {m_input}: user password changed successfully.")
    else:
        print(Fore.RED + "[!]: Invald input")


def sudo_file():
    print(
        """
            1. Add to sudo 
            2. Remove from sudo 
    """
    )

    s_input = int(input("[sudoAction]: Enter you command: "))

    if s_input == 2:
        u_name = input("[sudoAction]: Enter user name: ")
        if u_name != "" and sudo_password != "":
            # Create a subprocess object to run the 'deluser' command
            p = subprocess.Popen(
                ["sudo", "-S", "deluser", u_name, "sudo"],
                stdin=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
            )

            # get password and send to the subprocess
            sudo_password = getpass.getpass(prompt="[sudo]: sudo password: ")
            stderr, stdout = p.communicate(sudo_password + "\n")

            # check the error message if any error found
            if p.returncode != 0:
                print(Fore.RED + f"[!] :{stdout}!")

            else:
                print(
                    Fore.GREEN + f"[+] {u_name}: user removed from sudo successfully."
                )
        else:
            print(Fore.RED + "[-]: Empty input.")

    elif s_input == 1:
        u_name = input("[sudoAction]: Enter user name: ")
        if u_name != "" and sudo_password != "":
            # Create a subprocess object to run the 'useradd' command
            p = subprocess.Popen(
                ["sudo", "-S", "adduser", u_name, "sudo"],
                stdin=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
            )

            # get password and send to the subprocess
            sudo_password = getpass.getpass(prompt="[sudo]: sudo password: ")
            stderr, stdout = p.communicate(sudo_password + "\n")

            # check the error message if any error found
            if p.returncode != 0:
                print(Fore.RED + f"[!] :{stdout}!")

            else:
                print(Fore.GREEN + f"[+] {u_name}: user added to sudo successfully.")

        else:
            print(Fore.RED + "[!]: User name is empty.")

    else:
        print(Fore.RED + "[!]: Invalid input!")


while True:
    try:
        print(options())
        user_input = int(input("Enter your command: "))

        if user_input == 1:
            u_name = input("[addUser]: New user name: ")
            u_pass = getpass.getpass(prompt="[addUser]: New user password: ")

            if u_name and u_pass:
                add(u_name, u_pass)
            else:
                print(Fore.RED + "[!]: Invalid credentials.")

        elif user_input == 2:
            modify()

        elif user_input == 3:
            sudo_file()

        elif user_input == 4:
            users_list()

        elif user_input == 5:
            o_name = input("[deleteUser]: Enter user name: ")
            if o_name:
                delete(o_name)
        elif user_input == 6:
            break
        else:
            print(Fore.RED + "[-]: Invalid input!")

    # error handle
    except KeyboardInterrupt:
        break
    except FileNotFoundError:
        print(Fore.YELLOW + "[!]: This program is made for only linux.")
    except ValueError:
        print(Fore.RED + "[-]: Please select the right input!")
