import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpHeaders } from "@angular/common/http"; 
import { throwError } from "rxjs";
import { Router } from '@angular/router';

@Component({
  selector: 'app-signin',
  templateUrl: './signin.component.html',
  styleUrl: './signin.component.css'
})
export class SigninComponent {
  username: string
  password: string
  msg : string

  constructor(private httpClient: HttpClient, private router: Router) { }
  ngOnInit() {
    const apiUrl = 'http://localhost:5000/';
    // Send a POST request to the server
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*'
    });
    const upload$ = this.httpClient.post(apiUrl, null, {withCredentials: true, headers:headers});
    upload$.subscribe({  
      next: (data:any) => {
        if (data.msg=="connected") {
          this.router.navigate(['/dashboard']);
        }
      },
      error: (error: any) => {
        return throwError(() => error);
      },
    });
  }
  
  onSubmit() {
    const apiUrl = 'http://localhost:5000/signin';
    const postData = { username: this.username, password: this.password };
    // Send a POST request to the server

    const headers = new HttpHeaders({
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
    });

    this.msg = "Connecting..."
    const upload$ = this.httpClient.post(apiUrl, postData, {withCredentials: true, headers:headers});

    upload$.subscribe({  
      next: (data : any) => {
        if (data.msg=="success") {
          this.router.navigate(['/dashboard']);
        } else {
          this.msg = data.msg;
        }
      },
      error: (error: any) => {
        return throwError(() => error);
      },
    });
  }
}
