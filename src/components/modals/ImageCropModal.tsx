import React, { useState, useRef, useEffect, useCallback } from 'react';
import ReactCrop, {
  centerCrop,
  makeAspectCrop,
  type Crop,
  type PixelCrop,
} from 'react-image-crop';

interface ImageCropModalProps {
  isOpen: boolean;
  onClose: () => void;
  imageSrc: string | null;
  onCropComplete: (croppedImage: string) => void;
}

function getCroppedImg(image: HTMLImageElement, crop: PixelCrop): string {
    const canvas = document.createElement('canvas');
    const scaleX = image.naturalWidth / image.width;
    const scaleY = image.naturalHeight / image.height;

    canvas.width = crop.width;
    canvas.height = crop.height;

    const ctx = canvas.getContext('2d');
    if (!ctx) {
        throw new Error('Could not get canvas context');
    }

    ctx.drawImage(
        image,
        crop.x * scaleX,
        crop.y * scaleY,
        crop.width * scaleX,
        crop.height * scaleY,
        0,
        0,
        crop.width,
        crop.height
    );

    return canvas.toDataURL('image/jpeg');
}

const ASPECT_RATIOS = [
  { value: 1, text: '1:1' },
  { value: 4 / 3, text: '4:3' },
  { value: 16 / 9, text: '16:9' },
  { value: undefined, text: 'Free' },
];


export const ImageCropModal: React.FC<ImageCropModalProps> = ({
  isOpen,
  onClose,
  imageSrc,
  onCropComplete,
}) => {
  const imgRef = useRef<HTMLImageElement>(null);
  const [crop, setCrop] = useState<Crop>();
  const [completedCrop, setCompletedCrop] = useState<PixelCrop>();
  const [aspect, setAspect] = useState<number | undefined>(1);

  // Reset aspect to default when modal is opened
  useEffect(() => {
    if (isOpen) {
        setAspect(1);
    }
  }, [isOpen]);

  const onImageLoad = useCallback((img: HTMLImageElement) => {
    const { width, height } = img;
    const a = aspect ?? 1;
    const newCrop = centerCrop(
      makeAspectCrop(
        {
          unit: "%",
          width: 90,
        },
        a,
        width,
        height,
      ),
      width,
      height,
    );
    setCrop(newCrop);
    setCompletedCrop(undefined); // Clear completed crop on new image or aspect change
  }, [aspect]);
  
  // Recalculate crop when aspect changes
  useEffect(() => {
    if (imgRef.current) {
        onImageLoad(imgRef.current);
    }
  }, [aspect, onImageLoad]);


  const handleCrop = () => {
    if (completedCrop?.width && completedCrop?.height && imgRef.current) {
      const croppedImageUrl = getCroppedImg(imgRef.current, completedCrop);
      onCropComplete(croppedImageUrl);
    }
  };

  if (!isOpen || !imageSrc) {
    return null;
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-60 flex items-center justify-center z-[100] p-4" aria-modal="true" role="dialog">
      <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-2xl w-full max-w-2xl max-h-[90vh] flex flex-col animate-fade-in-up">
        <header className="flex items-center justify-between p-6 border-b border-gray-200 dark:border-gray-700">
          <h2 className="text-2xl font-bold text-gray-800 dark:text-gray-100">Adjust Photo</h2>
          <button onClick={onClose} className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors text-3xl font-light" aria-label="Close modal">&times;</button>
        </header>
        
        <main className="flex-1 p-6 overflow-y-auto flex flex-col justify-center items-center">
            <div className="flex flex-wrap justify-center items-center gap-2 mb-4 pdf-hide">
                <span className="text-sm font-medium self-center mr-2 text-gray-600 dark:text-gray-300">Aspect Ratio:</span>
                {ASPECT_RATIOS.map(ratio => (
                <button
                    key={ratio.text}
                    onClick={() => setAspect(ratio.value)}
                    className={`px-3 py-1 text-sm font-semibold rounded-md transition-colors ${
                    aspect === ratio.value
                        ? 'bg-primary text-white shadow-sm'
                        : 'bg-gray-200 text-gray-700 hover:bg-gray-300 dark:bg-gray-700 dark:text-gray-200 dark:hover:bg-gray-600'
                    }`}
                >
                    {ratio.text}
                </button>
                ))}
            </div>
          <ReactCrop
            crop={crop}
            onChange={(_: unknown, percentCrop: Crop) => setCrop(percentCrop)}
            onComplete={(c: PixelCrop) => setCompletedCrop(c)}
            aspect={aspect}
            circularCrop={aspect === 1}
          >
            <img
              ref={imgRef}
              alt="Crop me"
              src={imageSrc}
              onLoad={(e) => onImageLoad(e.currentTarget)}
              style={{ maxHeight: '65vh' }}
            />
          </ReactCrop>
        </main>
        
        <footer className="p-6 bg-gray-50 dark:bg-gray-800/50 border-t border-gray-200 dark:border-gray-700 rounded-b-2xl flex justify-end gap-3">
            <button onClick={onClose} className="px-4 py-2 text-sm font-semibold text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-100 transition-colors dark:bg-gray-700 dark:text-gray-200 dark:border-gray-600 dark:hover:bg-gray-600">Cancel</button>
            <button 
                onClick={handleCrop} 
                disabled={!completedCrop?.width || !completedCrop?.height}
                className="px-4 py-2 text-sm font-semibold text-white bg-primary rounded-lg hover:bg-blue-600 transition-colors disabled:bg-gray-300 disabled:cursor-not-allowed shadow-sm dark:disabled:bg-gray-600"
            >
                Crop & Save
            </button>
        </footer>
      </div>
    </div>
  );
};
