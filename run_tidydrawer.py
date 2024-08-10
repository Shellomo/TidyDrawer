# File: run_tidydrawer.py

import os
from tidydrawer.core.engine import TidyDrawerEngine


def main():
    # Specify the folder to process
    folder_to_process = 'test_folder'  # Adjust this path as needed
    # Load the template
    template_path = os.path.join('templates', 'to_types.yaml')  # Adjust this path as needed

    # Initialize the engine
    engine = TidyDrawerEngine(folder_to_process)

    engine.load_template(template_path)

    # Process the folder
    results = engine.process_folder(folder_to_process)

    # Print the results
    print(f"Processed {len(results)} files:")
    for result in results:
        print(f"File: {result['file']}")
        print(f"  Matched Rule: {result['matched_rule']}")
        print(f"  Action Performed: {result['action_performed']}")
        print("--------------------")

    # input("Press Enter to undo all actions...")
    # To undo all actions
    print("Undoing all actions...")
    undo_results = engine.undo_all_actions()
    print("Undo done.")
    # print(undo_results)


if __name__ == "__main__":
    main()