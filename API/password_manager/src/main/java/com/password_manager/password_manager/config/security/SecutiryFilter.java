package com.password_manager.password_manager.config.security;

import com.password_manager.password_manager.models.UserModel;
import com.password_manager.password_manager.services.UserServices;
import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

import java.io.IOException;
import java.util.Collections;

@SuppressWarnings("ALL")
@Component
public class SecutiryFilter extends OncePerRequestFilter {

    private final UserServices userServices;
    private final TokenService tokenService;

    public SecutiryFilter(UserServices userServices, TokenService tokenService) {
        this.userServices = userServices;
        this.tokenService = tokenService;
    }

    @Override
    public void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain filterChain) throws ServletException, IOException {
        String token = this.recoverToken(request);
        String login = this.tokenService.validateToken(token);

        if (login != null) {
            UserModel userModel = this.userServices.findByEmail(login).orElseThrow(() -> new RuntimeException("User not found!"));
            var authorities = Collections.singleton(new SimpleGrantedAuthority(userModel.getRole().toString()));
            var authentication = new UsernamePasswordAuthenticationToken(userModel, null, authorities);
            SecurityContextHolder.getContext().setAuthentication(authentication);
        }
        filterChain.doFilter(request, response);
    }

    public String recoverToken(HttpServletRequest request) {
        var authHeader = request.getHeader("Authorization");
        if (authHeader == null) return null;
        return authHeader.replace("Bearer ", "");
    }
}
