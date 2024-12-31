'use client';

import { useState, useEffect } from 'react';
import { Plus, Trash2, FileText } from 'lucide-react';
import { Button } from "@/components/ui/button";
import { knowledgeApi, Dataset } from '@/api/endpoints/knowledge';
import Link from 'next/link';
import { useToast } from "@/hooks/use-toast";

export default function KnowledgePage() {
  const [datasets, setDatasets] = useState<Dataset[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { toast } = useToast();

  useEffect(() => {
    fetchDatasets();
  }, []);

  const fetchDatasets = async () => {
    setLoading(true);
    try {
      const response = await knowledgeApi.getDatasets();
      setDatasets(response);
    } catch (err) {
      console.error('Error fetching datasets:', err);
      setError('Failed to load datasets');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: string) => {
    try {
      await knowledgeApi.deleteDataset(id);
      toast({
        title: "Success",
        description: "Dataset deleted successfully",
      });
      fetchDatasets();
    } catch (err) {
      toast({
        variant: "destructive",
        title: "Error",
        description: "Failed to delete dataset",
      });
    }
  };

  return (
    <div className="container max-w-7xl mx-auto p-6">
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold">Knowledge Base</h1>
          <p className="text-muted-foreground mt-1">Manage your training documents and datasets</p>
        </div>
        <Link href="/knowledge/upload">
          <Button className="flex items-center gap-2">
            <Plus className="h-4 w-4" />
            Upload New Dataset
          </Button>
        </Link>
      </div>

      <div className="rounded-lg border bg-card">
        {loading && (
          <div className="p-8 text-center text-muted-foreground">
            Loading datasets...
          </div>
        )}

        {error && (
          <div className="p-8 text-center text-red-500">
            {error}
          </div>
        )}

        {!loading && !error && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 p-4">
            {datasets.map((dataset) => (
              <div
                key={dataset.id}
                className="group block p-4 rounded-lg border hover:border-primary hover:shadow-sm transition-all"
              >
                <div className="flex items-start space-x-4">
                  <div className="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center">
                    <FileText className="h-6 w-6 text-primary" />
                  </div>
                  <div className="flex-1">
                    <div className="flex items-center justify-between">
                      <h3 className="font-medium group-hover:text-primary transition-colors">
                        {dataset.name || 'Unnamed Dataset'}
                      </h3>
                      <Button
                        variant="ghost"
                        size="icon"
                        className="opacity-0 group-hover:opacity-100 transition-opacity"
                        onClick={() => handleDelete(dataset.id)}
                      >
                        <Trash2 className="h-4 w-4 text-destructive" />
                      </Button>
                    </div>
                    <div className="text-sm text-muted-foreground">
                      Created by: {dataset.created_by || 'Unknown'}
                    </div>
                  </div>
                </div>
              </div>
            ))}

            {datasets.length === 0 && (
              <div className="col-span-full p-8 text-center text-muted-foreground">
                <div className="max-w-sm mx-auto">
                  <h3 className="font-medium mb-2">No datasets yet</h3>
                  <p className="text-sm mb-4">Upload your first document to start building your knowledge base.</p>
                  <Link href="/knowledge/upload">
                    <Button>
                      <Plus className="h-4 w-4 mr-2" />
                      Upload Dataset
                    </Button>
                  </Link>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}