import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpHeaders } from "@angular/common/http";  
import { throwError } from "rxjs";
import { Router } from '@angular/router';

@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrl: './signup.component.css'
})
export class SignupComponent {
  username: string
  password: string
  confirmpassword: string
  msg: string
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
    const apiUrl = 'http://localhost:5000/signup';
    const postData = { username: this.username, password: this.password, confirmpassword: this.confirmpassword };
    // Send a POST request to the server
    const headers = new HttpHeaders({
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
    });
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
