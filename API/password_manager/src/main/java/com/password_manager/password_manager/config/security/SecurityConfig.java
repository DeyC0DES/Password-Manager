package com.password_manager.password_manager.config.security;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpMethod;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.config.annotation.authentication.configuration.AuthenticationConfiguration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.annotation.web.configurers.AbstractHttpConfigurer;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.encrypt.Encryptors;
import org.springframework.security.crypto.encrypt.TextEncryptor;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;

@Configuration
@EnableWebSecurity
public class SecurityConfig {

    @Autowired
    private CustomUserDetailsService userDetailsService;

    @Autowired
    private SecutiryFilter secutiryFilter;

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        return http
                .csrf(AbstractHttpConfigurer::disable)
                .sessionManagement(session -> session.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
                .authorizeHttpRequests(authorize -> authorize
                        .requestMatchers(HttpMethod.POST, "/passwordManager/api/user/register").permitAll()
                        .requestMatchers(HttpMethod.POST, "/passwordManager/api/user/login").permitAll()
                        .requestMatchers(HttpMethod.POST, "/passwordManager/api/user/forget").permitAll()
                        .requestMatchers(HttpMethod.POST, "/passwordManager/api/user/forget/verification").permitAll()
                        .requestMatchers(HttpMethod.POST, "/passwordManager/api/user/2steps/verification").permitAll()
                        .requestMatchers(HttpMethod.POST, "/passwordManager/api/user/settings/verification").authenticated()
                        .requestMatchers(HttpMethod.POST, "/passwordManager/api/user/delete/send-code").authenticated()
                        .requestMatchers(HttpMethod.POST, "/passwordManager/api/account/create").authenticated()
                        .requestMatchers(HttpMethod.GET, "/passwordManager/api/account/getAccounts").authenticated()
                        .requestMatchers(HttpMethod.GET, "/passwordManager/api/account/decode/password").authenticated()
                        .requestMatchers(HttpMethod.PUT, "/passwordManager/api/account/update").authenticated()
                        .requestMatchers(HttpMethod.PUT, "/passwordManager/api/account/update/password").authenticated()
                        .requestMatchers(HttpMethod.PUT, "/passwordManager/api/user/update").authenticated()
                        .requestMatchers(HttpMethod.DELETE, "/passwordManager/api/account/delete").authenticated()
                        .requestMatchers(HttpMethod.DELETE, "/passwordManager/api/user/delete/verification").authenticated()
                        .anyRequest().permitAll()
                )
                .addFilterBefore(secutiryFilter, UsernamePasswordAuthenticationFilter.class)
                .build();
    }

    @Bean
    public TextEncryptor textEncryptor() {
        return Encryptors.delux("e7c8a1baf7e2d890f98f907cf4b5b116", "12345678");
    }

    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }

    @Bean
    public AuthenticationManager authenticationManager(AuthenticationConfiguration authenticationConfiguration) throws Exception {
        return authenticationConfiguration.getAuthenticationManager();
    }

}
