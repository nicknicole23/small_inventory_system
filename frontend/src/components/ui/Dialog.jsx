import React from 'react';
import { X } from 'lucide-react';
import { cn } from '../../lib/utils';
import { Button } from './Button';

const Dialog = ({ isOpen, onClose, title, children }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm">
      <div className="relative w-full max-w-lg rounded-lg bg-white p-6 shadow-lg animate-in fade-in zoom-in duration-200">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold leading-none tracking-tight">{title}</h2>
          <Button
            variant="ghost"
            size="icon"
            className="h-6 w-6 rounded-full p-0"
            onClick={onClose}
          >
            <X className="h-4 w-4" />
            <span className="sr-only">Close</span>
          </Button>
        </div>
        <div>{children}</div>
      </div>
    </div>
  );
};

export { Dialog };
