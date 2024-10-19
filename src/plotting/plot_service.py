from src.plotting.querry_gpt import querry_gpt
import os

# get the root directory which is two levels up
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

def plot(analysis_id: int, data: str, query: str):
    script = querry_gpt(query, data)
    # save scrip to temp.py
    with open(f'{root_dir}/temp.py', 'w') as f:
        f.write(script)
    # run the script dynamically, wait for it to finish
    os.system(f'python {root_dir}/temp.py')
    #exec(script)
    os.replace(f'{root_dir}/result.png', f'{root_dir}/src/UI/analyses/{analysis_id}.png')
    
if __name__ == '__main__':
    plot(1, "{}", "Test")
    