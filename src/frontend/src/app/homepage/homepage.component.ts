import { Component, OnInit } from '@angular/core';
import { HttpClient } from "@angular/common/http"; 
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
}
