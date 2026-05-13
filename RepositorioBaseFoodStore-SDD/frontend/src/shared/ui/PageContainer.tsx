import React from 'react';
import { HelpButton } from './HelpButton';

interface PageContainerProps {
  title: string;
  description?: string;
  helpContent?: React.ReactNode;
  actions?: React.ReactNode;
  children: React.ReactNode;
}

export const PageContainer: React.FC<PageContainerProps> = ({
  title,
  description,
  helpContent,
  actions,
  children,
}) => {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 animate-in fade-in duration-300">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-8">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl sm:text-3xl font-bold text-gray-900 tracking-tight">{title}</h1>
            {helpContent && <HelpButton content={helpContent} />}
          </div>
          {description && <p className="mt-1 text-gray-500">{description}</p>}
        </div>
        {actions && <div className="flex items-center gap-3 shrink-0">{actions}</div>}
      </div>
      {children}
    </div>
  );
};
