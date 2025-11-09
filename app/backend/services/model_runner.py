"""
Model runner that executes the actual optimization model
This script properly imports classes and runs the feedback loop
"""
import sys
import os
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

def run_optimization_model(
    piece_information_csv: str,
    flight_information_csv: str,
    load_locations_csv: str,
    pax_information_csv: str,
    buildup_information_csv: str,
    arrival_airport: str,
    restricted_locations: list = None,
    model_type: str = "delgado_venezian"
):
    """
    Run the actual optimization model
    
    Args:
        piece_information_csv: Path to PieceInformation.csv
        flight_information_csv: Path to FlightInformation.csv
        load_locations_csv: Path to LoadLocations.csv
        pax_information_csv: Path to PaxInformation.csv
        buildup_information_csv: Path to BuildUpInformation.csv
        arrival_airport: Arrival airport code
        restricted_locations: List of restricted load locations
        model_type: Type of model to run
    
    Returns:
        Dictionary with optimization results
    """
    if restricted_locations is None:
        restricted_locations = []
    
    # Change to project root to execute notebooks
    original_cwd = os.getcwd()
    os.chdir(PROJECT_ROOT)
    
    try:
        # Import classes by executing the notebook code
        # We'll use exec to run the notebook cells
        
        # First, read and execute Classes.ipynb
        classes_code = _extract_python_from_notebook(PROJECT_ROOT / "Classes.ipynb")
        exec_globals = {}
        exec(classes_code, exec_globals)
        
        # Read and execute Spotfire_Data_Extraction.ipynb (if needed)
        spotfire_code = _extract_python_from_notebook(PROJECT_ROOT / "Spotfire_Data_Extraction.ipynb")
        exec(spotfire_code, exec_globals)
        
        # Now setup the project
        ProjectSetup = exec_globals.get('ProjectSetup')
        if not ProjectSetup:
            raise ImportError("Could not import ProjectSetup class")
        
        project_setup = ProjectSetup()
        
        # Determine baseline/optimized_actual/bax_fixed flags
        baseline = model_type == "baseline"
        optimized_actual = model_type == "optimized_actual"
        bax_fixed = model_type == "bax_fixed"
        
        # Setup project
        cargo, aircraft, EP, plot, data_analysis = project_setup.setup_project(
            piece_information_csv,
            flight_information_csv,
            load_locations_csv,
            pax_information_csv,
            buildup_information_csv,
            arrival_airport,
            restricted_locations,
            baseline=baseline,
            optimized_actual=optimized_actual,
            BAX_fixed=bax_fixed
        )
        
        # Import the model solving function
        if model_type == "delgado_venezian":
            model_code = _extract_python_from_notebook(PROJECT_ROOT / "Model.ipynb")
        elif model_type == "baseline":
            model_code = _extract_python_from_notebook(PROJECT_ROOT / "Baseline.ipynb")
        elif model_type == "optimized_actual":
            model_code = _extract_python_from_notebook(PROJECT_ROOT / "Optimized_Actual.ipynb")
        elif model_type == "bax_fixed":
            model_code = _extract_python_from_notebook(PROJECT_ROOT / "BAX_Fixed.ipynb")
        else:
            model_code = _extract_python_from_notebook(PROJECT_ROOT / "Model.ipynb")
        
        exec(model_code, exec_globals)
        
        # Get the feedback_loop function
        feedback_loop = exec_globals.get('feedback_loop')
        if not feedback_loop:
            raise ImportError("Could not import feedback_loop function")
        
        # Make aircraft and other objects available
        exec_globals['aircraft'] = aircraft
        exec_globals['cargo'] = cargo
        exec_globals['EP'] = EP
        exec_globals['plot'] = plot
        exec_globals['project_setup'] = project_setup
        
        # Run the feedback loop
        feedback_loop(cargo)
        
        # Extract results from the model
        # The results are stored in the cargo and aircraft objects
        results = {
            'cargo': cargo,
            'aircraft': aircraft,
            'success': True
        }
        
        return results
        
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        return {
            'success': False,
            'error': str(e),
            'traceback': error_trace
        }
    finally:
        os.chdir(original_cwd)


def _extract_python_from_notebook(notebook_path: Path) -> str:
    """Extract Python code from a Jupyter notebook"""
    try:
        import nbformat
        
        with open(notebook_path, 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)
        
        code_cells = []
        for cell in nb.cells:
            if cell.cell_type == 'code':
                source = cell.source
                # Skip magic commands that won't work in exec
                if not source.strip().startswith('%'):
                    code_cells.append(source)
        
        return '\n\n'.join(code_cells)
        
    except ImportError:
        # Fallback: read as raw text if nbformat not available
        with open(notebook_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Try to extract code cells manually (simplified)
            import json
            nb_data = json.loads(content)
            code_cells = []
            for cell in nb_data.get('cells', []):
                if cell.get('cell_type') == 'code':
                    source = ''.join(cell.get('source', []))
                    if not source.strip().startswith('%'):
                        code_cells.append(source)
            return '\n\n'.join(code_cells)
    except Exception as e:
        raise Exception(f"Error reading notebook {notebook_path}: {e}")

