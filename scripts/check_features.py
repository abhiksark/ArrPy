#!/usr/bin/env python3
"""
Feature matrix checker for ArrPy.
Shows which operations are implemented in each backend.
"""

import sys
import os
from typing import Dict, List, Tuple
from tabulate import tabulate
import importlib

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import arrpy
from arrpy import Backend, set_backend, get_backend


class FeatureChecker:
    """Check which features are implemented in each backend."""
    
    def __init__(self):
        self.backends = ['python', 'cython', 'c']
        self.categories = {
            'Basic Operations': [
                ('Addition (a + b)', self.check_add),
                ('Subtraction (a - b)', self.check_subtract),
                ('Multiplication (a * b)', self.check_multiply),
                ('Division (a / b)', self.check_divide),
                ('Power (a ** b)', self.check_power),
                ('Modulo (a % b)', self.check_mod),
                ('Negative (-a)', self.check_neg),
                ('Absolute (abs)', self.check_abs),
            ],
            'Linear Algebra': [
                ('Matrix multiply (@)', self.check_matmul),
                ('Dot product', self.check_dot),
                ('Transpose', self.check_transpose),
                ('Inverse', self.check_inv),
                ('Determinant', self.check_det),
                ('Solve Ax=b', self.check_solve),
                ('Eigenvalues', self.check_eig),
                ('SVD', self.check_svd),
                ('QR decomposition', self.check_qr),
                ('Cholesky', self.check_cholesky),
            ],
            'Reductions': [
                ('Sum', self.check_sum),
                ('Mean', self.check_mean),
                ('Min', self.check_min),
                ('Max', self.check_max),
                ('Product', self.check_prod),
                ('Argmin', self.check_argmin),
                ('Argmax', self.check_argmax),
                ('Standard deviation', self.check_std),
                ('Variance', self.check_var),
            ],
            'Universal Functions': [
                ('Sin', self.check_sin),
                ('Cos', self.check_cos),
                ('Tan', self.check_tan),
                ('Exp', self.check_exp),
                ('Log', self.check_log),
                ('Log10', self.check_log10),
                ('Sqrt', self.check_sqrt),
                ('Square', self.check_square),
            ],
            'Array Creation': [
                ('zeros', self.check_zeros),
                ('ones', self.check_ones),
                ('eye', self.check_eye),
                ('arange', self.check_arange),
                ('linspace', self.check_linspace),
                ('array', self.check_array),
                ('full', self.check_full),
                ('empty', self.check_empty),
            ],
            'Indexing & Slicing': [
                ('Basic indexing [i]', self.check_basic_indexing),
                ('Slicing [i:j]', self.check_slicing),
                ('Negative indexing [-i]', self.check_negative_indexing),
                ('Step slicing [::2]', self.check_step_slicing),
                ('Boolean indexing', self.check_boolean_indexing),
                ('Fancy indexing', self.check_fancy_indexing),
                ('Where', self.check_where),
            ],
            'Sorting & Searching': [
                ('Sort', self.check_sort),
                ('Argsort', self.check_argsort),
                ('Unique', self.check_unique),
                ('Searchsorted', self.check_searchsorted),
                ('Partition', self.check_partition),
            ],
            'Statistics': [
                ('Median', self.check_median),
                ('Percentile', self.check_percentile),
                ('Cumsum', self.check_cumsum),
                ('Cumprod', self.check_cumprod),
                ('Diff', self.check_diff),
                ('Gradient', self.check_gradient),
                ('Clip', self.check_clip),
            ],
            'Array Manipulation': [
                ('Reshape', self.check_reshape),
                ('Flatten', self.check_flatten),
                ('Concatenate', self.check_concatenate),
                ('Stack', self.check_stack),
                ('Split', self.check_split),
                ('Squeeze', self.check_squeeze),
                ('Expand dims', self.check_expand_dims),
            ],
        }
        
    def check_operation(self, backend: str, operation) -> str:
        """Check if an operation works in a given backend."""
        try:
            set_backend(backend)
            operation()
            return "✅"
        except NotImplementedError:
            return "❌"
        except Exception as e:
            # Some other error - might be partial implementation
            if "not implemented" in str(e).lower():
                return "❌"
            return "⚠️"  # Warning - partially implemented or has issues
    
    # Basic Operations
    def check_add(self):
        a = arrpy.array([1, 2, 3])
        b = arrpy.array([4, 5, 6])
        c = a + b
        
    def check_subtract(self):
        a = arrpy.array([1, 2, 3])
        b = arrpy.array([4, 5, 6])
        c = a - b
        
    def check_multiply(self):
        a = arrpy.array([1, 2, 3])
        b = arrpy.array([4, 5, 6])
        c = a * b
        
    def check_divide(self):
        a = arrpy.array([1, 2, 3])
        b = arrpy.array([4, 5, 6])
        c = a / b
        
    def check_power(self):
        a = arrpy.array([1, 2, 3])
        c = a ** 2
        
    def check_mod(self):
        a = arrpy.array([5, 6, 7])
        b = arrpy.array([2, 3, 4])
        c = a % b
        
    def check_neg(self):
        a = arrpy.array([1, 2, 3])
        c = -a
        
    def check_abs(self):
        a = arrpy.array([-1, -2, 3])
        c = arrpy.abs(a)
    
    # Linear Algebra
    def check_matmul(self):
        a = arrpy.array([[1, 2], [3, 4]])
        b = arrpy.array([[5, 6], [7, 8]])
        c = a @ b
        
    def check_dot(self):
        a = arrpy.array([1, 2, 3])
        b = arrpy.array([4, 5, 6])
        c = arrpy.dot(a, b)
        
    def check_transpose(self):
        a = arrpy.array([[1, 2], [3, 4]])
        c = arrpy.transpose(a)
        
    def check_inv(self):
        a = arrpy.array([[1, 2], [3, 4]])
        c = arrpy.inv(a)
        
    def check_det(self):
        a = arrpy.array([[1, 2], [3, 4]])
        c = arrpy.det(a)
        
    def check_solve(self):
        a = arrpy.array([[1, 2], [3, 4]])
        b = arrpy.array([5, 6])
        c = arrpy.solve(a, b)
        
    def check_eig(self):
        a = arrpy.array([[1, 2], [3, 4]])
        vals, vecs = arrpy.eig(a)
        
    def check_svd(self):
        a = arrpy.array([[1, 2], [3, 4]])
        u, s, vt = arrpy.svd(a)
        
    def check_qr(self):
        a = arrpy.array([[1, 2], [3, 4]])
        q, r = arrpy.qr(a)
        
    def check_cholesky(self):
        a = arrpy.array([[4, 2], [2, 3]])
        L = arrpy.cholesky(a)
    
    # Reductions
    def check_sum(self):
        a = arrpy.array([1, 2, 3, 4, 5])
        s = a.sum()
        
    def check_mean(self):
        a = arrpy.array([1, 2, 3, 4, 5])
        m = a.mean()
        
    def check_min(self):
        a = arrpy.array([1, 2, 3, 4, 5])
        m = a.min()
        
    def check_max(self):
        a = arrpy.array([1, 2, 3, 4, 5])
        m = a.max()
        
    def check_prod(self):
        a = arrpy.array([1, 2, 3, 4, 5])
        p = a.prod()
        
    def check_argmin(self):
        a = arrpy.array([3, 1, 4, 1, 5])
        i = a.argmin()
        
    def check_argmax(self):
        a = arrpy.array([3, 1, 4, 1, 5])
        i = a.argmax()
        
    def check_std(self):
        a = arrpy.array([1, 2, 3, 4, 5])
        s = arrpy.std(a)
        
    def check_var(self):
        a = arrpy.array([1, 2, 3, 4, 5])
        v = arrpy.var(a)
    
    # Universal Functions
    def check_sin(self):
        a = arrpy.array([0, 1, 2])
        s = arrpy.sin(a)
        
    def check_cos(self):
        a = arrpy.array([0, 1, 2])
        c = arrpy.cos(a)
        
    def check_tan(self):
        a = arrpy.array([0, 1, 2])
        t = arrpy.tan(a)
        
    def check_exp(self):
        a = arrpy.array([0, 1, 2])
        e = arrpy.exp(a)
        
    def check_log(self):
        a = arrpy.array([1, 2, 3])
        l = arrpy.log(a)
        
    def check_log10(self):
        a = arrpy.array([1, 10, 100])
        l = arrpy.log10(a)
        
    def check_sqrt(self):
        a = arrpy.array([1, 4, 9])
        s = arrpy.sqrt(a)
        
    def check_square(self):
        a = arrpy.array([1, 2, 3])
        s = arrpy.square(a)
    
    # Array Creation
    def check_zeros(self):
        a = arrpy.zeros((3, 3))
        
    def check_ones(self):
        a = arrpy.ones((3, 3))
        
    def check_eye(self):
        a = arrpy.eye(3)
        
    def check_arange(self):
        a = arrpy.arange(10)
        
    def check_linspace(self):
        a = arrpy.linspace(0, 1, 10)
        
    def check_array(self):
        a = arrpy.array([1, 2, 3])
        
    def check_full(self):
        a = arrpy.full((3, 3), 5)
        
    def check_empty(self):
        a = arrpy.empty((3, 3))
    
    # Indexing & Slicing
    def check_basic_indexing(self):
        a = arrpy.array([1, 2, 3, 4, 5])
        b = a[2]
        
    def check_slicing(self):
        a = arrpy.array([1, 2, 3, 4, 5])
        b = a[1:4]
        
    def check_negative_indexing(self):
        a = arrpy.array([1, 2, 3, 4, 5])
        b = a[-1]
        
    def check_step_slicing(self):
        a = arrpy.array([1, 2, 3, 4, 5])
        b = a[::2]
        
    def check_boolean_indexing(self):
        a = arrpy.array([1, 2, 3, 4, 5])
        mask = a > 2
        b = arrpy.boolean_index(a, mask)
        
    def check_fancy_indexing(self):
        a = arrpy.array([1, 2, 3, 4, 5])
        indices = arrpy.array([0, 2, 4])
        b = arrpy.fancy_index(a, indices)
        
    def check_where(self):
        a = arrpy.array([1, 2, 3, 4, 5])
        b = arrpy.where(a > 2, a, 0)
    
    # Sorting & Searching
    def check_sort(self):
        a = arrpy.array([3, 1, 4, 1, 5])
        s = arrpy.sort(a)
        
    def check_argsort(self):
        a = arrpy.array([3, 1, 4, 1, 5])
        i = arrpy.argsort(a)
        
    def check_unique(self):
        a = arrpy.array([1, 2, 2, 3, 3, 3])
        u = arrpy.unique(a)
        
    def check_searchsorted(self):
        a = arrpy.array([1, 2, 3, 4, 5])
        i = arrpy.searchsorted(a, 3)
        
    def check_partition(self):
        a = arrpy.array([3, 1, 4, 1, 5])
        p = arrpy.partition(a, 2)
    
    # Statistics
    def check_median(self):
        a = arrpy.array([1, 2, 3, 4, 5])
        m = arrpy.median(a)
        
    def check_percentile(self):
        a = arrpy.array([1, 2, 3, 4, 5])
        p = arrpy.percentile(a, 50)
        
    def check_cumsum(self):
        a = arrpy.array([1, 2, 3, 4, 5])
        c = arrpy.cumsum(a)
        
    def check_cumprod(self):
        a = arrpy.array([1, 2, 3, 4, 5])
        c = arrpy.cumprod(a)
        
    def check_diff(self):
        a = arrpy.array([1, 2, 4, 7, 11])
        d = arrpy.diff(a)
        
    def check_gradient(self):
        a = arrpy.array([1, 2, 4, 7, 11])
        g = arrpy.gradient(a)
        
    def check_clip(self):
        a = arrpy.array([1, 2, 3, 4, 5])
        c = arrpy.clip(a, 2, 4)
    
    # Array Manipulation
    def check_reshape(self):
        a = arrpy.array([1, 2, 3, 4, 5, 6])
        r = a.reshape(2, 3)
        
    def check_flatten(self):
        a = arrpy.array([[1, 2], [3, 4]])
        f = a.flatten()
        
    def check_concatenate(self):
        a = arrpy.array([1, 2, 3])
        b = arrpy.array([4, 5, 6])
        c = arrpy.concatenate([a, b])
        
    def check_stack(self):
        a = arrpy.array([1, 2, 3])
        b = arrpy.array([4, 5, 6])
        s = arrpy.stack([a, b])
        
    def check_split(self):
        a = arrpy.array([1, 2, 3, 4, 5, 6])
        parts = arrpy.split(a, 3)
        
    def check_squeeze(self):
        a = arrpy.array([[[1, 2, 3]]])
        s = arrpy.squeeze(a)
        
    def check_expand_dims(self):
        a = arrpy.array([1, 2, 3])
        e = arrpy.expand_dims(a, axis=0)
    
    def generate_matrix(self) -> Dict[str, Dict[str, List[Tuple[str, str]]]]:
        """Generate the feature matrix."""
        matrix = {}
        
        for category, operations in self.categories.items():
            matrix[category] = {}
            for backend in self.backends:
                matrix[category][backend] = []
                for op_name, op_func in operations:
                    status = self.check_operation(backend, op_func)
                    matrix[category][backend].append((op_name, status))
        
        # Reset to Python backend
        set_backend('python')
        return matrix
    
    def print_matrix(self, matrix: Dict[str, Dict[str, List[Tuple[str, str]]]]):
        """Print the feature matrix in a nice format."""
        print("\n" + "="*80)
        print("                    ArrPy Feature Matrix v1.0.0")
        print("="*80)
        print("  ✅ = Fully implemented  ❌ = Not implemented  ⚠️ = Partial/Issues")
        print("="*80)
        
        for category, backends_data in matrix.items():
            print(f"\n{'─'*80}")
            print(f"  {category}")
            print(f"{'─'*80}")
            
            # Prepare table data
            rows = []
            operations = backends_data['python']  # Get operation names from any backend
            
            for i, (op_name, _) in enumerate(operations):
                row = [op_name]
                for backend in self.backends:
                    status = backends_data[backend][i][1]
                    row.append(status)
                rows.append(row)
            
            # Print table
            headers = ['Operation'] + [b.upper() for b in self.backends]
            print(tabulate(rows, headers=headers, tablefmt='simple'))
        
        # Print summary statistics
        print("\n" + "="*80)
        print("                           Summary Statistics")
        print("="*80)
        
        total_by_backend = {b: 0 for b in self.backends}
        implemented_by_backend = {b: 0 for b in self.backends}
        
        for category, backends_data in matrix.items():
            for backend in self.backends:
                for _, status in backends_data[backend]:
                    total_by_backend[backend] += 1
                    if status == "✅":
                        implemented_by_backend[backend] += 1
        
        summary_rows = []
        for backend in self.backends:
            total = total_by_backend[backend]
            impl = implemented_by_backend[backend]
            percentage = (impl / total * 100) if total > 0 else 0
            summary_rows.append([
                backend.upper(),
                f"{impl}/{total}",
                f"{percentage:.1f}%"
            ])
        
        print(tabulate(summary_rows, 
                      headers=['Backend', 'Implemented', 'Coverage'],
                      tablefmt='simple'))
        
        print("\n" + "="*80)
        print("  Use 'make features' to regenerate this matrix")
        print("  Use 'make features-detailed' for more detailed output")
        print("="*80)


def main():
    """Main function to run the feature checker."""
    import argparse
    parser = argparse.ArgumentParser(description='Check ArrPy feature implementation matrix')
    parser.add_argument('--detailed', action='store_true', 
                       help='Show detailed output including warnings')
    parser.add_argument('--backend', choices=['python', 'cython', 'c'],
                       help='Check only a specific backend')
    parser.add_argument('--category', 
                       help='Check only a specific category')
    parser.add_argument('--json', action='store_true',
                       help='Output as JSON')
    
    args = parser.parse_args()
    
    checker = FeatureChecker()
    
    # Generate the matrix
    print("Checking feature implementations...")
    matrix = checker.generate_matrix()
    
    # Output the results
    if args.json:
        import json
        # Convert to JSON-serializable format
        json_matrix = {}
        for cat, backends in matrix.items():
            json_matrix[cat] = {}
            for backend, ops in backends.items():
                json_matrix[cat][backend] = {op: status for op, status in ops}
        print(json.dumps(json_matrix, indent=2))
    else:
        checker.print_matrix(matrix)


if __name__ == "__main__":
    main()