import torch
from torch.utils.data import Dataset, DataLoader
from transformers import BertTokenizerFast, BertForSequenceClassification, Trainer, TrainingArguments
import json
import os

os.environ["CUDA_VISIBLE_DEVICES"] = "0"

class QuestionStatementDataset(Dataset):
    def __init__(self, file, tokenizer, max_length=128):
        self.sentences = []
        self.labels = []
        self.tokenizer = tokenizer
        self.max_length = max_length

        with open(file, 'r') as f:
            data = [json.loads(line) for line in f]
        
        for item in data:
            self.sentences.append(item['sentence'])
            # 0 for 'declarative', 1 for 'interrogative'
            self.labels.append(0 if item['type'] == 'declarative' else 1)

    def __len__(self):
        return len(self.sentences)

    def __getitem__(self, idx):
        encoding = self.tokenizer(self.sentences[idx], truncation=True, max_length=self.max_length, padding='max_length')
        return {
            'input_ids': torch.tensor(encoding['input_ids'], dtype=torch.long),
            'attention_mask': torch.tensor(encoding['attention_mask'], dtype=torch.long),
            'labels': torch.tensor(self.labels[idx], dtype=torch.long)
        }

model_name_or_path = 'bert-base-uncased'
tokenizer = BertTokenizerFast.from_pretrained(model_name_or_path)
model = BertForSequenceClassification.from_pretrained(model_name_or_path, num_labels=2)

train_dataset = QuestionStatementDataset('train.jsonl', tokenizer)
val_dataset = QuestionStatementDataset('val.jsonl', tokenizer)

# Set training arguments
training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=3,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=64,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir='./logs',
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
)


trainer.train()
