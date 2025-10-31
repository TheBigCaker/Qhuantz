
import React from 'react';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  className?: string;
}

const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ label, className = '', id, ...props }, ref) => {
    return (
      <div className="w-full">
        {label && (
          <label htmlFor={id} className="block text-sm font-medium text-slate-300 mb-1">
            {label}
          </label>
        )}
        <input
          id={id}
          ref={ref}
          className={`w-full bg-slate-900/50 border border-slate-600 rounded-md px-3 py-2 text-slate-100 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-violet-500 focus:border-violet-500 transition ${className}`}
          {...props}
        />
      </div>
    );
  }
);

Input.displayName = 'Input';
export default Input;
