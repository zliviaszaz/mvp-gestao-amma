import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { FormsModule } from '@angular/forms';

interface Participante { id: string; nome: string; data_nascimento?: string | null; telefone?: string | null; status: string; }
interface Atividade { id: string; nome: string; descricao?: string | null; data_inicio: string; status: string; }

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent implements OnInit {
  private http = inject(HttpClient);
  readonly apiUrl = 'http://127.0.0.1:8000/api';
  participantes: Participante[] = [];
  atividades: Atividade[] = [];
  busca = '';
  mensagem = '';
  erro = '';
  aba: 'participantes' | 'atividades' = 'participantes';
  novoParticipante = { nome: '', data_nascimento: '', telefone: '' };
  novaAtividade = { nome: '', descricao: '', data_inicio: '' };

  ngOnInit(): void { this.carregarParticipantes(); this.carregarAtividades(); }

  carregarParticipantes(): void {
    const query = this.busca.trim() ? `?q=${encodeURIComponent(this.busca.trim())}` : '';
    this.http.get<Participante[]>(`${this.apiUrl}/participantes${query}`).subscribe({
      next: data => { this.participantes = data; this.erro = ''; },
      error: () => this.erro = 'Não foi possível carregar participantes. Verifique se a API está em execução.'
    });
  }

  carregarAtividades(): void {
    this.http.get<Atividade[]>(`${this.apiUrl}/atividades`).subscribe({
      next: data => this.atividades = data,
      error: () => this.erro = 'Não foi possível carregar atividades. Verifique se a API está em execução.'
    });
  }

  cadastrarParticipante(): void {
    this.mensagem = ''; this.erro = '';
    this.http.post<Participante>(`${this.apiUrl}/participantes`, {
      nome: this.novoParticipante.nome,
      data_nascimento: this.novoParticipante.data_nascimento || null,
      telefone: this.novoParticipante.telefone || null
    }).subscribe({
      next: () => {
        this.mensagem = 'Participante cadastrado com sucesso!';
        this.novoParticipante = { nome: '', data_nascimento: '', telefone: '' };
        this.carregarParticipantes();
      },
      error: err => this.erro = err.error?.detail || 'Não foi possível cadastrar. Confira os dados.'
    });
  }

  cadastrarAtividade(): void {
    this.mensagem = ''; this.erro = '';
    this.http.post<Atividade>(`${this.apiUrl}/atividades`, this.novaAtividade).subscribe({
      next: () => {
        this.mensagem = 'Atividade cadastrada com sucesso!';
        this.novaAtividade = { nome: '', descricao: '', data_inicio: '' };
        this.carregarAtividades();
      },
      error: err => this.erro = err.error?.detail || 'Não foi possível cadastrar a atividade.'
    });
  }
}
