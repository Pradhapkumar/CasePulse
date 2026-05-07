import React, { useState, useRef, useEffect } from 'react';
import { useLanguage } from '../../context/LanguageContext';
import { Globe, ChevronDown, Check } from 'lucide-react';

const LanguageSelector = () => {
  const { selectedLanguage, setSelectedLanguage, languageOptions } = useLanguage();
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef(null);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleSelect = (option) => {
    setSelectedLanguage(option);
    setIsOpen(false);
  };

  return (
    <div className="relative" ref={dropdownRef}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-2 px-3 py-2 rounded-lg border border-border bg-card hover:bg-accent/50 transition-colors"
      >
        <Globe size={18} className="text-muted-foreground" />
        <span className="hidden sm:inline-flex items-center gap-2 text-sm font-medium">
          <span className="opacity-70">{selectedLanguage.flag}</span>
          {selectedLanguage.native}
        </span>
        <ChevronDown size={14} className={`transition-transform duration-200 ${isOpen ? 'rotate-180' : ''}`} />
      </button>

      {isOpen && (
        <div className="absolute right-0 mt-2 w-56 max-h-96 overflow-y-auto rounded-xl border border-border bg-card shadow-lg z-50 py-2 animate-in fade-in zoom-in duration-200">
          <div className="px-3 py-2 text-xs font-semibold text-muted-foreground uppercase tracking-wider">
            Select Language
          </div>
          {languageOptions.map((option) => (
            <button
              key={option.code}
              onClick={() => handleSelect(option)}
              className={`w-full flex items-center justify-between px-3 py-2.5 text-sm hover:bg-accent transition-colors ${
                selectedLanguage.code === option.code ? 'text-primary bg-primary/5' : 'text-foreground'
              }`}
            >
              <div className="flex items-center gap-3">
                <span className="text-base">{option.flag}</span>
                <div className="flex flex-col items-start">
                  <span className="font-medium">{option.native}</span>
                  <span className="text-[10px] opacity-60 uppercase">{option.label}</span>
                </div>
              </div>
              {selectedLanguage.code === option.code && <Check size={16} />}
            </button>
          ))}
        </div>
      )}
    </div>
  );
};

export default LanguageSelector;
