import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpHeaders } from "@angular/common/http"; 
import { throwError } from "rxjs";
import { Router } from '@angular/router';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.css'
})
export class DashboardComponent {
  username: string;
  history: Array<string>;
  status: "initial" | "uploading" | "success" | "fail" = "initial"; // Variable to store file status
  progress: number = 0;
  file: File | null = null; // Variable to store file

  constructor(private httpClient: HttpClient, private router: Router) { }
  ngOnInit() {
    const apiUrl = 'http://localhost:5000/dashboard';
    // Send a POST request to the server
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*'
    });
    const upload$ = this.httpClient.post(apiUrl, null,{withCredentials: true, headers:headers});
    upload$.subscribe({  
      next: (data : any)=> {
        if (Object.keys(data).length === 0) {
          this.router.navigate(['/']);
        } else {
          this.username = data.userdata.username;
          this.history = data.userdata.history;
        }
      },
      error: (error: any) => {
        return throwError(() => error);
      },
    });
  }

  disconnect() {
     const apiUrl = 'http://localhost:5000/disconnect';
    // Send a POST request to the server
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*'
    });
    const upload$ = this.httpClient.post(apiUrl, null, {withCredentials: true, headers:headers});
    upload$.subscribe({  
      next: (data : any)=> {
          this.router.navigate(['/']);
      },
      error: (error: any) => {
        return throwError(() => error);
      },
    });   
  }

  // On file Select
  onUpload(event: any) {
    const file: File = event.target.files[0];
    if (file) {
      this.file = file;
      const formData = new FormData();

      formData.append('audio', this.file);
      const upload$ = this.httpClient.post("http://localhost:5000/convert", formData, {withCredentials: true});

      this.status = 'uploading';

      upload$.subscribe({  
        next: (data : any) => {
          this.status = data.msg;
        },
        error: (error: any) => {
          this.status = 'fail';
          return throwError(() => error);
        },
      });
    }
  }
}
