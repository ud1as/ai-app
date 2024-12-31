'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { useToast } from "@/hooks/use-toast";
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Progress } from '@/components/ui/progress';
import { Upload, FileText, AlertCircle, Check, ArrowLeft } from 'lucide-react';
import { knowledgeApi, DEFAULT_TENANT_ID, FilePreviewResponse, validateFile } from '@/api/endpoints/knowledge';
import Link from 'next/link';

export default function UploadPage() {
  const router = useRouter();
  const { toast } = useToast();
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<FilePreviewResponse | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleFileSelect = async (file: File) => {
    setError(null);
    try {
      validateFile(file);
      setFile(file);
      await handlePreview(file);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Error selecting file';
      setError(errorMessage);
      toast({
        variant: 'destructive',
        title: 'Error',
        description: errorMessage,
      });
    }
  };

  const handlePreview = async (selectedFile: File) => {
    setIsUploading(true);
    try {
      const response = await knowledgeApi.previewFile(selectedFile);
      setPreview(response);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Could not generate preview';
      setError(errorMessage);
      toast({
        variant: 'destructive',
        title: 'Preview Failed',
        description: errorMessage,
      });
    } finally {
      setIsUploading(false);
    }
  };

  const handleProcess = async () => {
    if (!file) return;
    
    setIsProcessing(true);
    try {
      const response = await knowledgeApi.processFile(file, DEFAULT_TENANT_ID);
      
      if (response.success) {
        toast({
          title: 'Success',
          description: 'File processed successfully',
        });
        router.push('/knowledge');
      } else {
        throw new Error(response.error || 'Processing failed');
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Error processing file';
      setError(errorMessage);
      toast({
        variant: 'destructive',
        title: 'Processing Failed',
        description: errorMessage,
      });
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="container max-w-4xl mx-auto py-6">
      <div className="mb-6">
        <Link href="/knowledge">
          <Button variant="ghost" className="flex items-center gap-2">
            <ArrowLeft className="h-4 w-4" />
            Back to Knowledge Base
          </Button>
        </Link>
      </div>
      
      <Card>
        <CardHeader>
          <CardTitle>Upload Dataset</CardTitle>
          <CardDescription>
            Upload documents to train your AI assistant. Supported formats: PDF, DOC, DOCX, TXT (up to 10MB)
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-6">
            {/* Upload Area */}
            <div
              onDragOver={(e) => e.preventDefault()}
              onDrop={(e) => {
                e.preventDefault();
                const droppedFile = e.dataTransfer.files[0];
                handleFileSelect(droppedFile);
              }}
              className={`
                border-2 border-dashed rounded-lg p-8
                ${error ? 'border-destructive' : 'border-border'}
                transition-colors duration-200
                hover:border-primary cursor-pointer
              `}
            >
              <div className="flex flex-col items-center text-center">
                <input
                  type="file"
                  id="file-upload"
                  className="hidden"
                  onChange={(e) => e.target.files?.[0] && handleFileSelect(e.target.files[0])}
                  accept=".pdf,.doc,.docx,.txt"
                />
                <label htmlFor="file-upload" className="cursor-pointer">
                  {file ? (
                    <div className="flex items-center gap-2">
                      <FileText className="h-6 w-6" />
                      <span>{file.name}</span>
                    </div>
                  ) : (
                    <div className="flex flex-col items-center gap-2">
                      <Upload className="h-8 w-8" />
                      <span>Drop your file here or click to browse</span>
                      <span className="text-sm text-muted-foreground">
                        PDF, DOC, DOCX, or TXT up to 10MB
                      </span>
                    </div>
                  )}
                </label>
              </div>
            </div>

            {/* Error Message */}
            {error && (
              <Alert variant="destructive">
                <AlertCircle className="h-4 w-4" />
                <AlertDescription>{error}</AlertDescription>
              </Alert>
            )}

            {/* Upload Progress */}
            {isUploading && (
              <div className="space-y-2">
                <Progress value={30} className="w-full" />
                <p className="text-sm text-center text-muted-foreground">
                  Analyzing document...
                </p>
              </div>
            )}

            {/* Preview Section */}
            {preview && (
              <div className="space-y-4">
                <div className="bg-muted rounded-lg p-4">
                  <div className="text-sm font-medium mb-2">
                    Document Preview ({preview.total_chunks} chunks)
                  </div>
                  <div className="space-y-3 max-h-60 overflow-y-auto">
                    {preview.chunks.map((chunk) => (
                      <div
                        key={chunk.chunk_index}
                        className="text-sm bg-background rounded p-2"
                      >
                        <div className="text-xs text-muted-foreground mb-1">
                          Chunk {chunk.chunk_index + 1} of {chunk.chunk_total}
                        </div>
                        <div className="whitespace-pre-wrap">{chunk.content}</div>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="flex justify-end">
                  <Button
                    onClick={handleProcess}
                    disabled={isProcessing}
                  >
                    {isProcessing ? (
                      <span className="flex items-center gap-2">
                        <Progress className="h-4 w-4" />
                        Processing...
                      </span>
                    ) : (
                      <span className="flex items-center gap-2">
                        <Check className="h-4 w-4" />
                        Process Document
                      </span>
                    )}
                  </Button>
                </div>
              </div>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}