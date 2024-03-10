import { Component, OnInit } from '@angular/core';
import { HttpClient } from "@angular/common/http"; 
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

  constructor(private httpClient: HttpClient, private router: Router) { }
  ngOnInit() {
    const apiUrl = 'http://app.default.svc.cluster.local:5000/';
    // Send a POST request to the server
    const upload$ = this.httpClient.post(apiUrl, {});
    upload$.subscribe({  
      next: data => {
        if (data=="connected") {
          this.router.navigate(['/dashboard']);
        }
      },
      error: (error: any) => {
        return throwError(() => error);
      },
    });
  }
  
  onSubmit() {
    const apiUrl = 'http://app.default.svc.cluster.local:5000/signin';
    const postData = { username: this.username, password: this.password };
    // Send a POST request to the server
    const upload$ = this.httpClient.post(apiUrl, postData);

    upload$.subscribe({  
      next: data => {
        this.router.navigate(['/dashboard']);
      },
      error: (error: any) => {
        return throwError(() => error);
      },
    });
  }
}
