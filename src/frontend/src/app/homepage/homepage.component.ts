import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpHeaders } from "@angular/common/http"; 
import { throwError } from "rxjs";
import { Router } from '@angular/router';

@Component({
  selector: 'app-homepage',
  templateUrl: './homepage.component.html',
  styleUrl: './homepage.component.css'
})
export class HomepageComponent {
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
      next: (data: any) => {
        if (data.msg=="connected") {
          this.router.navigate(['/dashboard']);
        }
      },
      error: (error: any) => {
        return throwError(() => error);
      },
    });
  }
}
