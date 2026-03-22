from controller import Controller
from utility import MSCPException


def main():
    try:
        num_tasks = 20
        num_subsets = 50
        num_subsets_to_select = 20

        print(f"Number of tasks (m): {num_tasks}")
        print(f"Number of subsets (n): {num_subsets}")
        print(f"Number of subsets to select (k): {num_subsets_to_select}")

        controller = Controller()
        controller.generate_instance(num_tasks, num_subsets, num_subsets_to_select)
        controller.write_problem_data()
        controller.add_problem_data_to_solver()

        solver = controller.get_solver()
        solver.prepare_model()
        solver.write_model(f"data/{controller.get_instance_name()}.mps")
        solver.solve()

    except MSCPException as e:
        print(f"EXCEPTION: {e}")


if __name__ == "__main__":
    main()
