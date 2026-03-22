import React, { useState, useEffect, useRef } from 'react';
import { PencilIcon, TrashIcon } from './icons';

interface EditableFieldProps {
  value: string;
  onSave: (value: string) => void;
  className?: string;
  as?: 'p' | 'h1' | 'h2' | 'h3' | 'span' | 'div';
  isTextArea?: boolean;
  disabled?: boolean;
  onDelete?: () => void;
}

export const EditableField: React.FC<EditableFieldProps> = ({
  value,
  onSave,
  className = '',
  as: Component = 'p',
  isTextArea = false,
  disabled = false,
  onDelete,
}) => {
  const [isEditing, setIsEditing] = useState(false);
  const [currentValue, setCurrentValue] = useState(value);
  const inputRef = useRef<HTMLInputElement | HTMLTextAreaElement>(null);

  useEffect(() => {
    setCurrentValue(value);
  }, [value]);

  useEffect(() => {
    if (isEditing) {
      inputRef.current?.focus();
      if (inputRef.current && 'select' in inputRef.current) {
        (inputRef.current as HTMLInputElement).select();
      }
    }
  }, [isEditing]);

  const handleSave = () => {
    if (currentValue.trim() !== value.trim()) {
      onSave(currentValue);
    }
    setIsEditing(false);
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !isTextArea) {
      handleSave();
    } else if (e.key === 'Escape') {
      setCurrentValue(value);
      setIsEditing(false);
    }
  };
  
  const handleEditClick = (e: React.MouseEvent) => {
    e.stopPropagation();
    if (!disabled) {
      setIsEditing(true);
    }
  };

  const handleDeleteClick = (e: React.MouseEvent) => {
    e.stopPropagation();
    if (onDelete && !disabled) {
      onDelete();
    }
  };

  if (isEditing && !disabled) {
    const commonProps = {
      ref: inputRef as any,
      value: currentValue,
      onChange: (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => setCurrentValue(e.target.value),
      onBlur: handleSave,
      onKeyDown: handleKeyDown,
      className: `w-full bg-yellow-200 border border-primary rounded-md p-1 -m-1 ${className} dark:bg-yellow-200/30 dark:text-gray-100 dark:border-blue-400`
    };
    return isTextArea ? (
      <textarea {...commonProps} rows={4} />
    ) : (
      <input type="text" {...commonProps} />
    );
  }

  return (
    <Component
      onClick={() => !disabled && setIsEditing(true)}
      className={`relative group ${!disabled ? 'cursor-pointer hover:bg-yellow-100 dark:hover:bg-yellow-200/20' : 'cursor-default'} rounded-md p-1 -m-1 transition-colors ${className}`}
      title={disabled ? "" : "Click to edit"}
    >
      {value || '...'}
      {!disabled && (
        <div className="pdf-hide absolute top-1/2 right-0 -translate-y-1/2 flex items-center bg-white dark:bg-gray-800 rounded-md shadow-sm border border-gray-200 dark:border-gray-600 opacity-0 group-hover:opacity-100 transition-opacity p-0.5 space-x-0.5 z-10">
          {onDelete && (
            <button onClick={handleDeleteClick} title="Delete item" className="p-1 text-gray-500 hover:text-accent dark:hover:text-red-400 rounded-sm transition-colors">
              <TrashIcon className="w-3.5 h-3.5" />
            </button>
          )}
          <button onClick={handleEditClick} title="Edit field" className="p-1 text-gray-500 hover:text-primary dark:hover:text-blue-400 rounded-sm transition-colors">
            <PencilIcon className="w-3.5 h-3.5" />
          </button>
        </div>
      )}
    </Component>
  );
};
