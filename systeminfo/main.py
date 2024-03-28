import platform
import psutil
import GPUtil
import subprocess
import os

def get_total_memory_size():
    memory_info = psutil.virtual_memory()
    return (memory_info.total/(2**(10*3)))

def get_system_info():
    #print("System Information:")
    system_info = platform.uname()
    ans={}
    ans['system'] = f"{system_info.system}"
    ans['node_name'] = f"{system_info.node}"
    ans['release'] = f"{system_info.release}"
    ans['version'] = f"{system_info.version}"
    ans['machine'] = f"{system_info.machine}"
    ans['processor'] = f"{system_info.processor}"
    return ans

def get_cpu_info():
    cpu_info = platform.processor()
    cpu_count = psutil.cpu_count(logical=False)
    logical_cpu_count = psutil.cpu_count(logical=True)

    #print("\nCPU Information:")
    ans = {}
    ans['processor'] = f"{cpu_info}"
    ans['physical_cores'] = f"{cpu_count}"
    ans['logical_cores'] = f"{logical_cpu_count}"
    return ans

def get_memory_info():
    memory_info = psutil.virtual_memory()

    #print("\nMemory Information: Unit : bytes")
    ans={}
    ans['total_memory'] = f"{memory_info.total}"
    ans['available_memory'] = f"{memory_info.available}"
    ans['used_memory'] = f"{memory_info.used}"
    ans['memory_utilization'] = f"{memory_info.percent:.2f}%"
    return ans

def get_disk_info():
    disk_info = psutil.disk_usage('/')

    #print("\nDisk Information: Unit : bytes")
    ans={}
    ans['total_disk_space'] = f"{disk_info.total}"
    ans['used_disk_space'] = f"{disk_info.used}"
    ans['free_disk_space'] = f"{disk_info.free}"
    ans['disk_space_utilization'] = f" {disk_info.percent:.2f}%"

#Only Nvidia GPU
def get_gpu_info():    

    gpus = GPUtil.getGPUs()
    ans={}

    if not gpus:
        print("\nNo GPU detected.")
        ans['0'] = f"no_gpu"
    else:
        ans['0'] = f"there_is_gpu"

        for i, gpu in enumerate(gpus):
            #print(f"\nGPU {i + 1} Information:")
            ans[f'{i+1}'] = {}
            ans[f'{i+1}']['id'] = f"{gpu.id}"
            ans[f'{i+1}']['name'] = f"{gpu.id}"
            ans[f'{i+1}']['driver'] = f"{gpu.id}"
            ans[f'{i+1}']['gpu_memory_total'] = f"{gpu.memoryTotal} MB"
            ans[f'{i+1}']['gpu_memory_free'] = f"{gpu.memoryFree} MB"
            ans[f'{i+1}']['gpu_memory_used'] = f"{gpu.memoryUsed} MB"
            ans[f'{i+1}']['gpu_load'] = f"{gpu.load*100}%"
            ans[f'{i+1}']['gpu_temperature'] = f"{gpu.temperature}°C"

def check_windows_shell():
    parent_process = psutil.Process(os.getppid()).name().lower()
    if 'cmd' in parent_process:
        return 'CMD'
    elif 'powershell' in parent_process:
        return 'PowerShell'
    else:
        return 'Unknown'

def get_extra():
    system_info = platform.uname()
    ans={}
    ans['system'] = f"{system_info.system}"
    try:
        if(system_info.system=='Darwin'):
            ans['system_name'] = "macOS"

            print('----------Apple Mac---------')
            r1 = subprocess.run(['system_profiler', 'SPHardwareDataType'],capture_output=True,text=True)
            ans['hardware'] = f"{r1.stdout}"
            r2 = subprocess.run(['system_profiler', 'SPDisplaysDataType'],capture_output=True,text=True)
            ans['display'] = f"{r2.stdout}"
            r3 = subprocess.run(['system_profiler', 'SPSoftwareDataType'],capture_output=True,text=True)
            ans['software'] = f"{r3.stdout}"

            for line in ans['software'].split('\n'):
                if ('System Version' in line):
                    ans['os_version']=f"{line[22:]}"
            return ans
        elif(system_info.system=='Linux'):
            ans['system_name'] = "Linux"

            print('-------Linux----------')
            r1 = subprocess.run(['lshw'],capture_output=True,text=True)
            ans["hardware"] = f"{r1.stdout}"
            r2 = subprocess.run(['lsb_release','-a'],capture_output=True,text=True)
            ans['software'] = f"{r2.stdout}"
            for line in ans['software'].split('\n'):
                if ('Description' in line):
                    ans['os_version']=f"{line[12:]}"
            return ans

        elif(system_info.system=='Windows'):
            ans['system_name'] = "Windows"

            prefix_exe='powershell.exe'
            print("Python is running in:", check_windows_shell(), "on Windows")
            ans['run_in'] = f"{check_windows_shell()}"
            r1 = subprocess.run([prefix_exe,'Get-WmiObject','Win32_Processor'],capture_output=True,text=True)
            #print(r1.stdout)
            r2 = subprocess.run([prefix_exe,'Get-WmiObject','Win32_PhysicalMemory'],capture_output=True,text=True)
            #print(r2.stdout)
            r3 = subprocess.run([prefix_exe,'Get-WmiObject','Win32_VideoController'],capture_output=True,text=True)
            #print(r3.stdout)
            r4 = subprocess.run([prefix_exe,'(Get-WmiObject Win32_OperatingSystem).Caption'],capture_output=True,text=True)
            #print(r4.stdout)
            ans['os_version'] = f"{r4.stdout}"
        
        return ans

    except:
        print("error!")
