FROM node:18-alpine as builder

COPY package.json .

RUN npm install --save

RUN mkdir src
RUN mkdir public

COPY src/. src
COPY public/. public
COPY tsconfig.json .

RUN npm run build

FROM nginx as nginx

COPY --from=builder /build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/

EXPOSE 3001

CMD ["/bin/bash", "-c", "nginx -g 'daemon off;'"]